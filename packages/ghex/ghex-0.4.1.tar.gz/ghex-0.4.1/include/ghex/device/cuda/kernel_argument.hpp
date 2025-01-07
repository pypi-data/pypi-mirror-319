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

#include <ghex/device/attributes.hpp>

namespace ghex
{
namespace device
{
/** @brief simple std::array-like class used to efficiently pass arguments to a cuda kernel */
template<class T, unsigned int N>
struct kernel_argument
{
    T m_data[N];

    GHEX_HOST kernel_argument& fill(const T* data, unsigned int size)
    {
        if (size > N)
            throw std::runtime_error(
                "static space too small " + std::to_string(N) + " < " + std::to_string(size));
        for (unsigned int i = 0; i < size; ++i) m_data[i] = data[i];
        return *this;
    }
    GHEX_FUNCTION T& operator[](unsigned int i) { return m_data[i]; }

    GHEX_FUNCTION T const& operator[](unsigned int i) const { return m_data[i]; }
};

template<unsigned int N, typename T>
kernel_argument<T, N>
make_kernel_arg(T* data, unsigned int size)
{
    return kernel_argument<T, N>().fill(data, size);
}

} // namespace device

} // namespace ghex
