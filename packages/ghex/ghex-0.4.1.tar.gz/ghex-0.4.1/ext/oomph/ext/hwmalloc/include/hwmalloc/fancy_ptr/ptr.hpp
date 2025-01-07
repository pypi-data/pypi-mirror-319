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

#include <hwmalloc/fancy_ptr/void_ptr.hpp>
#include <hwmalloc/fancy_ptr/const_void_ptr.hpp>
#include <hwmalloc/fancy_ptr/memfct_ptr.hpp>
#include <iterator>
#include <type_traits>

namespace hwmalloc
{
template<typename T, typename Block>
class hw_ptr
{
  private:
    friend class hw_void_ptr<Block, void*>;
    using this_type = hw_ptr<T, Block>;
    using void_ptr_t = hw_void_ptr<Block, void*>;
    using const_void_ptr_t = hw_void_ptr<Block, void const*>;

  private:
    void_ptr_t m_ptr;

  public: // iteator typedefs
    using value_type = T;
    using difference_type = std::ptrdiff_t;
    using pointer = T*;
    using reference = T&;
    using iterator_category = std::random_access_iterator_tag;

  public:
    constexpr hw_ptr() noexcept = default;
    constexpr hw_ptr(hw_ptr const&) noexcept = default;
    constexpr hw_ptr(std::nullptr_t) noexcept
    : m_ptr{nullptr}
    {
    }
    hw_ptr& operator=(hw_ptr const&) noexcept = default;
    hw_ptr& operator=(std::nullptr_t) noexcept
    {
        m_ptr = nullptr;
        return *this;
    }

    constexpr friend bool operator==(hw_ptr a, hw_ptr b) noexcept { return (a.m_ptr == b.m_ptr); }
    constexpr friend bool operator!=(hw_ptr a, hw_ptr b) noexcept { return (a.m_ptr != b.m_ptr); }

  public:
    reference operator*() const noexcept { return *reinterpret_cast<T*>(m_ptr.get()); }
    pointer   operator->() const noexcept { return reinterpret_cast<T*>(m_ptr.get()); }
    pointer   get() const noexcept { return reinterpret_cast<T*>(m_ptr.get()); }
#if HWMALLOC_ENABLE_DEVICE
    pointer device_ptr() const noexcept { return reinterpret_cast<T*>(m_ptr.device_ptr()); }
#endif

    // support for pointer to member function
    template<typename R, typename U, typename... Args>
    typename std::enable_if<std::is_same<U, T>::value && std::is_class<U>::value,
        const pmfc<R (U::*)(Args...)>>::type
    operator->*(R (U::*pmf)(Args...)) const noexcept
    {
        return {get(), pmf};
    }

    // support for pointer to const member function
    template<typename R, typename U, typename... Args>
    typename std::enable_if<std::is_same<U, T>::value && std::is_class<U>::value,
        const pmfc<R (U::*)(Args...) const>>::type
    operator->*(R (U::*pmf)(Args...) const) const noexcept
    {
        return {get(), pmf};
    }

    // support for pointer to member
    template<typename M, typename U>
    typename std::enable_if<std::is_same<U, T>::value && std::is_class<U>::value, M&>::type
    operator->*(M U::*pm) const noexcept
    {
        return get()->*pm;
    }

    constexpr explicit operator void_ptr_t() const noexcept { return m_ptr; }
    constexpr explicit operator const_void_ptr_t() const noexcept { return m_ptr; }
    // needed for std::allocator_traits::construct
    constexpr explicit operator void*() const noexcept { return m_ptr.get(); }
    constexpr          operator bool() const noexcept { return (bool)m_ptr; }

    auto        handle() const noexcept { return m_ptr.handle(); }
    const auto& handle_ref() const noexcept { return m_ptr.m_data.m_handle; }
    auto&       handle_ref() noexcept { return m_ptr.m_data.m_handle; }

  public: // iterator functions
    this_type& operator++() noexcept
    {
        m_ptr.m_data.m_ptr = get() + 1;
#if HWMALLOC_ENABLE_DEVICE
        if (m_ptr.device_ptr()) m_ptr.m_data.m_device_ptr = device_ptr() + 1;
#endif
        return *this;
    }

    this_type operator++(int) noexcept
    {
        auto tmp = *this;
        m_ptr.m_data.m_ptr = get() + 1;
#if HWMALLOC_ENABLE_DEVICE
        if (m_ptr.device_ptr()) m_ptr.m_data.m_device_ptr = device_ptr() + 1;
#endif
        return tmp;
    }

    this_type& operator+=(std::ptrdiff_t n) noexcept
    {
        m_ptr.m_data.m_ptr = get() + n;
#if HWMALLOC_ENABLE_DEVICE
        if (m_ptr.device_ptr()) m_ptr.m_data.m_device_ptr = device_ptr() + n;
#endif
        return *this;
    }

    template<typename I, std::enable_if_t<std::is_integral_v<I>, bool> = true>
    friend this_type operator+(this_type a, I n) noexcept { return (a += static_cast<std::ptrdiff_t>(n)); }

    this_type& operator--() noexcept
    {
        m_ptr.m_data.m_ptr = get() - 1;
#if HWMALLOC_ENABLE_DEVICE
        if (m_ptr.device_ptr()) m_ptr.m_data.m_device_ptr = device_ptr() - 1;
#endif
        return *this;
    }

    this_type operator--(int) noexcept
    {
        auto tmp = *this;
        m_ptr.m_data.m_ptr = get() - 1;
#if HWMALLOC_ENABLE_DEVICE
        if (m_ptr.device_ptr()) m_ptr.m_data.m_device_ptr = device_ptr() - 1;
#endif
        return tmp;
    }

    this_type& operator-=(std::ptrdiff_t n) noexcept
    {
        m_ptr.m_data.m_ptr = get() - n;
#if HWMALLOC_ENABLE_DEVICE
        if (m_ptr.device_ptr()) m_ptr.m_data.m_device_ptr = device_ptr() - n;
#endif
        return *this;
    }

    template<typename I, std::enable_if_t<std::is_integral_v<I>, bool> = true>
    friend this_type operator-(this_type a, I n) noexcept { return (a -= static_cast<std::ptrdiff_t>(n)); }

    friend difference_type operator-(this_type const& a, this_type const& b) noexcept
    {
        return (a.get() - b.get());
    }

    reference& operator[](std::size_t n) const noexcept { return *(get() + n); }

    void release() { m_ptr.m_data.release(); }
};

template<typename Block, typename VoidPtr>
template<typename T>
constexpr hw_void_ptr<Block, VoidPtr>&
hw_void_ptr<Block, VoidPtr>::operator=(hw_ptr<T, Block> const& ptr) noexcept
{
    return (*this = (this_type)ptr);
}

template<typename Block, class VoidPtr>
template<class T>
constexpr hw_void_ptr<Block, VoidPtr>::operator hw_ptr<T, Block>() const noexcept
{
    auto p = hw_ptr<T, Block>();
    p.m_ptr = *this;
    return p;
}

// These classes are not implemented by design. See void_ptr.hpp for implemenation of void pointers.
template<typename Block>
class hw_ptr<void, Block>
{
};
template<typename Block>
class hw_ptr<void const, Block>
{
};

} // namespace hwmalloc
