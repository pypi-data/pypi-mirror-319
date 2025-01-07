/*
 * ghex-org
 *
 * Copyright (c) 2014-2023, ETH Zurich
 * All rights reserved.
 *
 * Please, refer to the LICENSE file in the root directory.
 * SPDX-License-Identifier: BSD-3-Clause
 */
#pragma once

#include <hwmalloc/detail/block.hpp>
#include <hwmalloc/numa.hpp>
#if HWMALLOC_ENABLE_DEVICE
#include <hwmalloc/device.hpp>
#endif
#include <type_traits>
#include <boost/lockfree/stack.hpp>
#include <atomic>

namespace hwmalloc
{
namespace detail
{
template<typename Context>
class pool;

template<typename Context>
class segment
{
  public:
    using pool_type = pool<Context>;
    using region_traits_type = region_traits<Context>;
    using region_type = typename region_traits_type::region_type;
#if HWMALLOC_ENABLE_DEVICE
    using device_region_type = typename region_traits_type::device_region_type;
#endif
    using block = block_t<Context>;

    struct allocation_holder
    {
        numa_tools::allocation m;
        ~allocation_holder() noexcept { hwmalloc::numa().free(m); }
    };

#if HWMALLOC_ENABLE_DEVICE
    struct device_allocation_holder
    {
        void* m = nullptr;
        ~device_allocation_holder() noexcept
        {
            if (m) device_free(m);
        }
    };
#endif

  private:
    using stack_type = boost::lockfree::stack<block, boost::lockfree::fixed_sized<true>>;

    pool_type*        m_pool;
    std::size_t       m_block_size;
    std::size_t       m_num_blocks;
    allocation_holder m_allocation;
    region_type       m_region;
#if HWMALLOC_ENABLE_DEVICE
    device_allocation_holder            m_device_allocation;
    std::unique_ptr<device_region_type> m_device_region;
#endif
    stack_type        m_freed_stack;
    std::atomic<long> m_num_freed;

  public:
    template<typename Stack>
    segment(pool_type* pool, region_type&& region, numa_tools::allocation alloc,
        std::size_t block_size, Stack& free_stack)
    : m_pool{pool}
    , m_block_size{block_size}
    , m_num_blocks{alloc.size / block_size}
    , m_allocation{alloc}
    , m_region{std::move(region)}
    , m_freed_stack(m_num_blocks)
    , m_num_freed(0)
    {
        char* origin = (char*)m_allocation.m.ptr;
        for (std::size_t i = m_num_blocks; i > 0; --i)
        {
            block b{this, nullptr, origin + (i - 1) * block_size,
                m_region.get_handle((i - 1) * block_size, block_size)};
            while (!free_stack.push(b)) {}
        }
    }

#if HWMALLOC_ENABLE_DEVICE
    template<typename Stack>
    segment(pool_type* pool, region_type&& region, numa_tools::allocation alloc,
        device_region_type&& device_region, void* device_ptr, int device_id, std::size_t block_size,
        Stack& free_stack)
    : m_pool{pool}
    , m_block_size{block_size}
    , m_num_blocks{alloc.size / block_size}
    , m_allocation{alloc}
    , m_region{std::move(region)}
    , m_device_allocation{device_ptr}
    , m_device_region{new device_region_type(std::move(device_region))}
    , m_freed_stack(m_num_blocks)
    , m_num_freed(0)
    {
        char* origin = (char*)m_allocation.m.ptr;
        char* device_origin = (char*)m_device_allocation.m;
        for (std::size_t i = m_num_blocks; i > 0; --i)
        {
            block b{this, nullptr, origin + (i - 1) * block_size,
                m_region.get_handle((i - 1) * block_size, block_size),
                device_origin + (i - 1) * block_size,
                m_device_region->get_handle((i - 1) * block_size, block_size), device_id};
            while (!free_stack.push(b)) {}
        }
    }
#endif

    segment(segment const&) = delete;
    segment(segment&&) = delete;

    std::size_t block_size() const noexcept { return m_block_size; }
    std::size_t capacity() const noexcept { return m_num_blocks; }
    std::size_t numa_node() const noexcept { return m_allocation.m.node; }
    pool_type*  get_pool() const noexcept { return m_pool; }

    bool is_empty() const noexcept
    {
        return static_cast<std::size_t>(m_num_freed.load()) == m_num_blocks;
    }

    template<typename Stack>
    std::size_t collect(Stack& stack)
    {
        const auto consumed = m_freed_stack.consume_all(
            [&stack](block const& b)
            {
                while (!stack.push(b)) {}
            });
        m_num_freed.fetch_sub(consumed);
        return consumed;
    }

    void free(block const& b)
    {
        while (!m_freed_stack.push(b)) {}
        ++m_num_freed;
    }
};


template<typename Context>
void block_t<Context>::release_from_segment() const noexcept
{
    m_segment->get_pool()->free(*this);
}

} // namespace detail
} // namespace hwmalloc
