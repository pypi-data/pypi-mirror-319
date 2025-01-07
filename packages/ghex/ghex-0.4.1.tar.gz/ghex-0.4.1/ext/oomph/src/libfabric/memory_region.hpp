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

#include <hwmalloc/register.hpp>
//
#include <rdma/fabric.h>
#include <rdma/fi_domain.h>
//
#include <iostream>
#include <memory>
#include <utility>

#include "fabric_error.hpp"

// ------------------------------------------------------------------
// This section exists to make interoperabily/sharing of code
// between OOMPH/GHEX and HPX easier
#if __has_include("./print.hpp")
#include "print.hpp"
#define DEBUG     OOMPH_DP_ONLY
#define has_debug 1
#elif __has_include(<hpx/debugging/print.hpp>)
#include <hpx/debugging/print.hpp>
#include <hpx/rma/rma_fwd.hpp>
#define DEBUG(printer, Expr) HPX_DP_ONLY(printer, Expr)
#define has_debug 1
#else
#define DEBUG(printer, Expr)
#endif
// ------------------------------------------------------------------

#define NS_MEMORY oomph::libfabric

namespace NS_MEMORY
{

static NS_DEBUG::enable_print<false> mrn_deb("REGION_");

// This is the only part of the code that actually
// calls libfabric functions
struct region_provider
{
    // The internal memory region handle
    using provider_region = struct fid_mr;
    using provider_domain = struct fid_domain;

    // register region
    template<typename... Args>
    static inline int register_memory(Args&&... args)
    {
        return fi_mr_reg(std::forward<Args>(args)...);
    }

    // register region
    template<typename... Args>
    static inline int register_memory_attr(Args&&... args)
    {
        [[maybe_unused]] auto scp = NS_MEMORY::mrn_deb.scope(__func__, std::forward<Args>(args)...);
        //        int x = FI_HMEM_ROCR;
        //        fi_mr_regattr(struct fid_domain *domain, const struct fi_mr_attr *attr,
        //                    uint64_t flags, struct fid_mr **mr)
        return fi_mr_regattr(std::forward<Args>(args)...);
    }

    // unregister region
    static inline int unregister_memory(provider_region* region) { return fi_close(&region->fid); }

    // Default registration flags for this provider
    static inline constexpr int flags()
    {
        return FI_READ | FI_WRITE | FI_RECV | FI_SEND | FI_REMOTE_READ | FI_REMOTE_WRITE;
    }

    // Get the local descriptor of the memory region.
    static inline void* get_local_key(provider_region* const region) { return fi_mr_desc(region); }

    // Get the remote key of the memory region.
    static inline uint64_t get_remote_key(provider_region* const region)
    {
        return fi_mr_key(region);
    }
};

// --------------------------------------------------------------------
// This is a handle to a small chunk of memory that has been registered
// as part of a much larger allocation (a memory_segment)
struct memory_handle
{
    // --------------------------------------------------------------------
    using provider_region = region_provider::provider_region;

    // --------------------------------------------------------------------
    // Default constructor creates unusable handle(region)
    memory_handle()
    : address_{nullptr}
    , region_{nullptr}
    , size_{0}
    , used_space_{0}
    {
    }
    memory_handle(memory_handle const&) noexcept = default;
    memory_handle& operator=(memory_handle const&) noexcept = default;

    memory_handle(provider_region* region, unsigned char* addr,
        std::size_t size /*, uint32_t flags*/) noexcept
    : address_{addr}
    , region_{region}
    , size_{uint32_t(size)}
    , used_space_{0}
    {
        //            DEBUG(NS_MEMORY::mrn_deb,
        //                trace(NS_DEBUG::str<>("memory_handle"), *this));
    }

    // --------------------------------------------------------------------
    // move constructor, clear other region so that it is not unregistered twice
    memory_handle(memory_handle&& other) noexcept
    : address_{other.address_}
    , region_{std::exchange(other.region_, nullptr)}
    , size_{other.size_}
    , used_space_{other.used_space_}
    {
    }

    // --------------------------------------------------------------------
    // move assignment, clear other region so that it is not unregistered twice
    memory_handle& operator=(memory_handle&& other) noexcept
    {
        address_ = other.address_;
        region_ = std::exchange(other.region_, nullptr);
        size_ = other.size_;
        used_space_ = other.used_space_;
        return *this;
    }

    // --------------------------------------------------------------------
    // Return the address of this memory region block.
    inline unsigned char* get_address(void) const { return address_; }

    // --------------------------------------------------------------------
    // Get the local descriptor of the memory region.
    inline void* get_local_key(void) const { return region_provider::get_local_key(region_); }

    // --------------------------------------------------------------------
    // Get the remote key of the memory region.
    inline uint64_t get_remote_key(void) const { return region_provider::get_remote_key(region_); }

    // --------------------------------------------------------------------
    // Get the size of the memory chunk usable by this memory region,
    // this may be smaller than the value returned by get_length
    // if the region is a sub region (partial region) within another block
    inline uint64_t get_size(void) const { return size_; }

    // --------------------------------------------------------------------
    // Get the size used by a message in the memory region.
    inline uint32_t get_message_length(void) const { return used_space_; }

    // --------------------------------------------------------------------
    // Set the size used by a message in the memory region.
    inline void set_message_length(uint32_t length) { used_space_ = length; }

    // --------------------------------------------------------------------
    void release_region() noexcept { region_ = nullptr; }

    // --------------------------------------------------------------------
    // return the underlying libfabric region handle
    inline provider_region* get_region() const { return region_; }

    // --------------------------------------------------------------------
    // Deregister the memory region.
    // returns 0 when successful, -1 otherwise
    int deregister(void) const
    {
        if (region_ /*&& !get_user_region()*/)
        {
            DEBUG(NS_MEMORY::mrn_deb, trace(NS_DEBUG::str<>("release"), region_));
            //
            if (region_provider::unregister_memory(region_))
            {
                DEBUG(NS_MEMORY::mrn_deb, error("fi_close mr failed"));
                return -1;
            }
            else
            {
                DEBUG(NS_MEMORY::mrn_deb, trace(NS_DEBUG::str<>("de-Registered region"), *this));
            }
            region_ = nullptr;
        }
        return 0;
    }

    // --------------------------------------------------------------------
    friend std::ostream& operator<<(std::ostream& os, memory_handle const& region)
    {
        (void)region;
#if has_debug
        // clang-format off
            os /*<< "region "*/      << NS_DEBUG::ptr(&region)
               //<< " fi_region "  << NS_DEBUG::ptr(region.region_)
           << " address "    << NS_DEBUG::ptr(region.address_)
           << " size "       << NS_DEBUG::hex<6>(region.size_)
               //<< " used_space " << NS_DEBUG::hex<6>(region.used_space_/*size_*/)
               << " loc key "  << NS_DEBUG::ptr(region.region_ ? region_provider::get_local_key(region.region_) : nullptr)
               << " rem key " << NS_DEBUG::ptr(region.region_ ? region_provider::get_remote_key(region.region_) : 0);
        // clang-format on
#endif
        return os;
    }

  protected:
    // This gives the start address of this region.
    // This is the address that should be used for data storage
    unsigned char* address_;

    // The hardware level handle to the region (as returned from libfabric fi_mr_reg)
    mutable provider_region* region_;

    // The (maximum available) size of the memory buffer
    uint32_t size_;

    // Space used by a message in the memory region.
    // This may be smaller/less than the size available if more space
    // was allocated than it turns out was needed
    mutable uint32_t used_space_;
};

// --------------------------------------------------------------------
// a memory segment is a pinned block of memory that has been specialized
// by a particular region provider. Each provider (infiniband, libfabric,
// other) has a different definition for the object and the protection
// domain used to limit access.
// --------------------------------------------------------------------
struct memory_segment : public memory_handle
{
    using provider_domain = region_provider::provider_domain;
    using provider_region = region_provider::provider_region;
    using handle_type = memory_handle;

    // --------------------------------------------------------------------
    memory_segment(provider_region* region, unsigned char* address, unsigned char* base_address,
        uint64_t size)
    : memory_handle(region, address, size)
    , base_addr_(base_address)
    {
    }

    // --------------------------------------------------------------------
    // move constructor, clear other region
    memory_segment(memory_segment&& other) noexcept
    : memory_handle(std::move(other))
    , base_addr_{std::exchange(other.base_addr_, nullptr)}
    {
    }

    // --------------------------------------------------------------------
    // move assignment, clear other region
    memory_segment& operator=(memory_segment&& other) noexcept
    {
        memory_handle(std::move(other));
        region_ = std::exchange(other.region_, nullptr);
        return *this;
    }

    // --------------------------------------------------------------------
    // construct a memory region object by registering an existing address buffer
    // we do not cache local/remote keys here because memory segments are only
    // used by the heap to store chunks and the user will always receive
    // a memory_handle - which does have keys cached
    memory_segment(provider_domain* pd, const void* buffer, const uint64_t length, bool bind_mr, void *ep)
    {
        // an rma key counter to keep some providers (CXI) happy
        static std::atomic<std::uint64_t> key = 0;
        //
        address_ = static_cast<unsigned char*>(const_cast<void*>(buffer));
        size_ = length;
        used_space_ = length;
        region_ = nullptr;
        //
        base_addr_ = memory_handle::address_;
        DEBUG(NS_MEMORY::mrn_deb, trace(NS_DEBUG::str<>("memory_segment"), *this));

        int ret = region_provider::register_memory(pd, const_cast<void*>(buffer), length,
            region_provider::flags(), 0, key++, 0, &(region_), nullptr);
        if (ret) { throw libfabric::fabric_error(int(ret), "register_memory"); }
        else { DEBUG(NS_MEMORY::mrn_deb, trace(NS_DEBUG::str<>("Registered region"), *this)); }

        if (bind_mr)
        {
            ret = fi_mr_bind(region_, (struct fid*)ep, 0);
            if (ret) { throw libfabric::fabric_error(int(ret), "fi_mr_bind"); }
            else { DEBUG(NS_MEMORY::mrn_deb, trace(NS_DEBUG::str<>("Bound region"), *this)); }

            ret = fi_mr_enable(region_);
            if (ret) { throw libfabric::fabric_error(int(ret), "fi_mr_enable"); }
            else { DEBUG(NS_MEMORY::mrn_deb, trace(NS_DEBUG::str<>("Enabled region"), *this)); }
        }
    }

    // --------------------------------------------------------------------
    // destroy the region and memory according to flag settings
    ~memory_segment() { deregister(); }

    handle_type get_handle(std::size_t offset, std::size_t size) const noexcept
    {
        return memory_handle(region_, base_addr_ + offset, size);
    }

    // --------------------------------------------------------------------
    // Get the address of the base memory region.
    // This is the address of the memory allocated from the system
    inline unsigned char* get_base_address(void) const { return base_addr_; }

    // --------------------------------------------------------------------
    friend std::ostream& operator<<(std::ostream& os, memory_segment const& region)
    {
        (void)region;
#if has_debug
        // clang-format off
            os << *static_cast<const memory_handle*>(&region)
               << " base address " << NS_DEBUG::ptr(region.base_addr_);
        // clang-format on
#endif
        return os;
    }

  public:
    // this is the base address of the memory registered by this segment
    // individual memory_handles are offset from this address
    unsigned char* base_addr_;
};

} // namespace NS_MEMORY
