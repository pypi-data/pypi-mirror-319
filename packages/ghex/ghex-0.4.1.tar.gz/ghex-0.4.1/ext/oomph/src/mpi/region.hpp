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

// paths relative to backend
#include <handle.hpp>

namespace oomph
{
class region
{
  public:
    using handle_type = handle;

  private:
    void* m_ptr;

  public:
    region(void* ptr)
    : m_ptr{ptr}
    {
    }

    region(region const&) = delete;

    region(region&& r) noexcept
    : m_ptr{std::exchange(r.m_ptr, nullptr)}
    {
    }

    // get a handle to some portion of the region
    handle_type get_handle(std::size_t offset, std::size_t size)
    {
        return {(void*)((char*)m_ptr + offset), size};
    }
};

class rma_region
{
  public:
    using handle_type = handle;

  private:
    MPI_Comm m_comm;
    MPI_Win  m_win;
    void*    m_ptr;

  public:
    rma_region(MPI_Comm comm, MPI_Win win, void* ptr, std::size_t size)
    : m_comm{comm}
    , m_win{win}
    , m_ptr{ptr}
    {
        OOMPH_CHECK_MPI_RESULT(MPI_Win_attach(m_win, ptr, size));
    }

    rma_region(rma_region const&) = delete;

    rma_region(rma_region&& r) noexcept
    : m_comm{r.m_comm}
    , m_win{r.m_win}
    , m_ptr{std::exchange(r.m_ptr, nullptr)}
    {
    }

    ~rma_region()
    {
        if (m_ptr) MPI_Win_detach(m_win, m_ptr);
    }

    // get a handle to some portion of the region
    handle_type get_handle(std::size_t offset, std::size_t size)
    {
        return {(void*)((char*)m_ptr + offset), size};
    }
};
} // namespace oomph
