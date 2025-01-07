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

#include <oomph/communicator.hpp>

// paths relative to backend
#include <../context_base.hpp>
#include <../increment_guard.hpp>

namespace oomph
{
template<typename Communicator>
class communicator_base
{
  public:
    using pool_factory_type = util::pool_factory<detail::request_state>;
    using recursion_increment = increment_guard<std::size_t>;

  protected:
    context_base*     m_context;
    pool_factory_type m_req_state_factory;
    std::size_t       m_recursion_depth = 0u;

    communicator_base(context_base* ctxt)
    : m_context(ctxt)
    {
    }

  public:
    rank_type            rank() const noexcept { return m_context->rank(); }
    rank_type            size() const noexcept { return m_context->size(); }
    MPI_Comm             mpi_comm() const noexcept { return m_context->get_comm(); }
    rank_topology const& topology() const noexcept { return m_context->topology(); }
    void release() { m_context->deregister_communicator(static_cast<Communicator*>(this)); }
    bool is_local(rank_type rank) const noexcept { return topology().is_local(rank); }

    bool has_reached_recursion_depth() const noexcept
    {
        return m_recursion_depth > OOMPH_RECURSION_DEPTH;
    }

    recursion_increment recursion() noexcept { return {m_recursion_depth}; }
};
} // namespace oomph
