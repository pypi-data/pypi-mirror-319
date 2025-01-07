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

#include <ucp/api/ucp.h>

#ifdef NDEBUG
#define OOMPH_CHECK_UCX_RESULT(x)          x;
#define OOMPH_CHECK_UCX_RESULT_NOEXCEPT(x) x;
#else
#include <string>
#include <stdexcept>
#define OOMPH_CHECK_UCX_RESULT(x)                                                                  \
    if (x != UCS_OK)                                                                               \
        throw std::runtime_error("OOMPH Error: UCX Call failed " + std::string(#x) + " in " +      \
                                 std::string(__FILE__) + ":" + std::to_string(__LINE__));
#define OOMPH_CHECK_UCX_RESULT_NOEXCEPT(x)                                                         \
    if (x != UCX_OK)                                                                               \
    {                                                                                              \
        std::cerr << "OOMPH Error: UCX Call failed " << std::string(#x) << " in "                  \
                  << std::string(__FILE__) << ":" << std::to_string(__LINE__) << std::endl;        \
        std::terminate();                                                                          \
    }
#endif
