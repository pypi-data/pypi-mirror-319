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

#include <utility>
#include <tuple>
#include <gridtools/common/layout_map.hpp>
#include <ghex/device/attributes.hpp>

namespace ghex
{

template<typename Tuple, typename Func, std::size_t... Is>
void
for_each_impl(Tuple&& t, Func&& f, std::index_sequence<Is...>)
{
    using std::get;
    (f(Is, get<Is>(t)), ...);
}

/**
 * @brief iterate over tuple type using a functor
 * @tparam Tuple tuple-like type
 * @tparam Func functor with signature void(auto& x), where x is tuple element
 * @param t tuple instance
 * @param f functor instance
 */
template<typename Tuple, typename Func>
void
for_each(Tuple&& t, Func&& f)
{
    using size = std::tuple_size<std::remove_reference_t<Tuple>>;
    for_each_impl(std::forward<Tuple>(t), std::forward<Func>(f),
        std::make_index_sequence<size::value>());
}

template<typename Tuple1, typename Tuple2, typename Func, std::size_t... Is>
void
for_each_impl(Tuple1&& t1, Tuple2&& t2, Func&& f, std::index_sequence<Is...>)
{
    using std::get;
    (f(Is, get<Is>(t1), get<Is>(t2)), ...);
}

/**
 * @brief iterate over two tuple types using a functor
 * @tparam Tuple1 tuple-like type
 * @tparam Tuple2 tuple-like type
 * @tparam Func functor with signature void(auto& x1, auto& x2), where x1, x2 are elements of t1 and t2
 * @param t1 tuple instance
 * @param t2 tuple instance
 * @param f functor instance
 */
template<typename Tuple1, typename Tuple2, typename Func>
void
for_each(Tuple1&& t1, Tuple2&& t2, Func&& f)
{
    using size = std::tuple_size<std::remove_reference_t<Tuple1>>;
    static_assert(size::value == std::tuple_size<std::remove_reference_t<Tuple2>>::value);
    for_each_impl(std::forward<Tuple1>(t1), std::forward<Tuple2>(t2), std::forward<Func>(f),
        std::make_index_sequence<size::value>());
}

// forward declaration
template<int D, int I, typename Layout, int Skip = 0>
struct for_loop;

/** @brief compile time recursive generation of loop nest for a D-dimensional array
 *
 * This template class provides compile time recursive nesting of D for-loops
 * and calls a function at the end of the iteration with the current D-dimensional coordinate
 * of the loop iteration.
 *
 * @tparam D dimensionality of loop nest
 * @tparam I I==D to start recursion
 * @tparam Layout template meta function which determines order of nesting
 * @tparam Skip the number of innermost loops to skip */
template<int D, int I, int... Args, int Skip>
struct for_loop<D, I, gridtools::layout_map<Args...>, Skip>
{
  private: // member types
    using layout_t = gridtools::layout_map<Args...>;
    using idx = std::integral_constant<int, layout_t::find(D - I)>;
    friend struct for_loop<D, I + 1, layout_t, Skip>;

  public: // static member functions
    /**
     * @brief generate loop nest
     * @tparam Func functor with signature void(x_0,x_1,...) where x_i are coordinates
     * @tparam Array coordinate vector type
     * @param f instance of functor
     * @param first start coordinate
     * @param last end coordinate (inclusive)
     */
    template<typename Func, typename Array>
    GHEX_FORCE_INLINE static void apply(Func&& f, Array&& first, Array&& last) noexcept
    {
        for (auto i = first[idx::value]; i <= last[idx::value]; ++i)
        {
            //std::remove_const_t<std::remove_reference_t<Array>> x{};
            std::remove_const_t<std::remove_reference_t<Array>> x = first;
            x[idx::value] = i;
            for_loop<D, I - 1, layout_t, Skip>::apply(std::forward<Func>(f),
                std::forward<Array>(first), std::forward<Array>(last), x);
        }
    }

  private: // implementation details
    template<typename Func, typename Array, typename Array2>
    GHEX_FORCE_INLINE static void apply(Func&& f, Array&& first, Array&& last, Array2&& y) noexcept
    {
        for (auto i = first[idx::value]; i <= last[idx::value]; ++i)
        {
            std::remove_const_t<std::remove_reference_t<Array2>> x{y};
            x[idx::value] = i;
            for_loop<D, I - 1, layout_t, Skip>::apply(std::forward<Func>(f),
                std::forward<Array>(first), std::forward<Array>(last), x);
        }
    }
};

// end of recursion
template<int D, int... Args, int Skip>
struct for_loop<D, Skip, gridtools::layout_map<Args...>, Skip>
{
  private: // member types
    using layout_t = gridtools::layout_map<Args...>;
    friend struct for_loop<D, Skip + 1, layout_t, Skip>;

  private: // implementation details
    template<typename Func, typename Array, typename Array2>
    GHEX_FORCE_INLINE static void apply(Func&& f, Array&&, Array&&, Array2&& x) noexcept
    {
        apply(std::forward<Func>(f), std::forward<Array2>(x), std::make_index_sequence<D>{});
    }

    template<typename Func, typename Array, std::size_t... Is>
    GHEX_FORCE_INLINE static void apply(Func&& f, Array&& x, std::index_sequence<Is...>)
    {
        // functor is called with expanded coordinates
        f(x[Is]...);
    }
};

// forward declaration
template<int D, int I, typename Layout>
struct for_loop_pointer_arithmetic;

/** @brief generation of loop nest for an D-dimensional array assuming contiguous memory 
 *
 * This template class provides compile time recursive nesting of D for-loops
 * and calls a function at the end of the iteration with the following 2 argments
 * - offset in a global D-dimensional array
 * - offset in a flattened buffer of the size of the accumulated iteration space the loop nest spans.
 *
 * @tparam D dimensionality of loop nest
 * @tparam I I==D to start recursion
 * @tparam Args compile time list of integral constants indicating order of loop nest*/
template<int D, int I, int... Args>
struct for_loop_pointer_arithmetic<D, I, gridtools::layout_map<Args...>>
{
  private: // member types
    using layout_t = gridtools::layout_map<Args...>;
    using idx = std::integral_constant<int, layout_t::find(D - I)>;
    friend class for_loop_pointer_arithmetic<D, I + 1, layout_t>;

  public: // static member functions
    /**
     * @brief generate loop nest
     * @tparam Func functor type with signature void(std::size_t, std::size_t)
     * @tparam Array coordinate vector type
     * @tparam Array2 coordinate difference vector type
     * @param f functor instance
     * @param first first coordinate in loop nest
     * @param last last coordinate in loop nest
     * @param extent extent of multi-dimensional array of which [first, last] is a sub-region
     * @param coordinate_offset distance from first coordinate in the multi-dimensional array to the origin (0,0,...).
     * An array without buffer zones has a coordinate offset of (0,0,...), while the offset is (1,1,...) for an array with buffer zone of 1.
     */
    template<typename Func, typename Array, typename Strides, typename Array2>
    GHEX_FORCE_INLINE static void apply(Func&& f, Array&& first, Array&& last,
        Strides&& byte_strides, Array2&& coordinate_offset) noexcept
    {
        std::size_t iter = 0;
        for (auto i = first[idx::value]; i <= last[idx::value]; ++i, ++iter)
        {
            for_loop_pointer_arithmetic<D, I - 1, layout_t>::apply(std::forward<Func>(f),
                std::forward<Array>(first), std::forward<Array>(last),
                std::forward<Strides>(byte_strides), std::forward<Array2>(coordinate_offset),
                (i + coordinate_offset[idx::value]) * byte_strides[idx::value], iter);
        }
    }

  private: // implementation details
    template<typename Func, typename Array, typename Strides, typename Array2>
    GHEX_FORCE_INLINE static void apply(Func&& f, Array&& first, Array&& last,
        Strides&& byte_strides, Array2&& coordinate_offset, std::size_t offset,
        std::size_t iter) noexcept
    {
        //offset *= extent[idx::value];
        iter *= last[idx::value] - first[idx::value] + 1;
        for (auto i = first[idx::value]; i <= last[idx::value]; ++i, ++iter)
        {
            for_loop_pointer_arithmetic<D, I - 1, layout_t>::apply(std::forward<Func>(f),
                std::forward<Array>(first), std::forward<Array>(last),
                std::forward<Strides>(byte_strides), std::forward<Array2>(coordinate_offset),
                offset + (i + coordinate_offset[idx::value]) * byte_strides[idx::value], iter);
        }
    }
};

// end of recursion
template<int D, int... Args>
struct for_loop_pointer_arithmetic<D, 0, gridtools::layout_map<Args...>>
{
    using layout_t = gridtools::layout_map<Args...>;
    template<typename Func, typename Array, typename Strides, typename Array2>
    GHEX_FORCE_INLINE static void apply(Func&& f, Array&&, Array&&, Strides&& byte_strides,
        Array2&&, std::size_t offset, std::size_t iter) noexcept
    {
        // functor call with two arguments
        // argument 1: offset in global multi-dimensional array
        // argument 2: offset within region defined by [first, last]
        using idx0 = std::integral_constant<int, layout_t::find(D - 1)>;
        f(offset, iter * byte_strides[idx0::value]);
    }
};

// forward declaration
template<typename Tuple>
struct transform;

// transform a tuple of types into another tuple of types
template<template<typename...> class Tuple, typename... Ts>
struct transform<Tuple<Ts...>>
{
    // by applying the compile-time transform CT
    template<template<typename> class CT>
    using with = Tuple<CT<Ts>...>;
};

} // namespace ghex
