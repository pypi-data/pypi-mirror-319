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
#include <endpoint.hpp>

namespace oomph
{
struct type_erased_address_db_t
{
    struct iface
    {
        virtual rank_type rank() = 0;
        virtual rank_type size() = 0;
        virtual int       est_size() = 0;
        virtual void      init(const address_t&) = 0;
        virtual address_t find(rank_type) = 0;
        virtual ~iface() {}
    };

    template<typename Impl>
    struct impl_t final : public iface
    {
        Impl m_impl;
        impl_t(const Impl& impl)
        : m_impl{impl}
        {
        }
        impl_t(Impl&& impl)
        : m_impl{std::move(impl)}
        {
        }
        rank_type rank() override { return m_impl.rank(); }
        rank_type size() override { return m_impl.size(); }
        int       est_size() override { return m_impl.est_size(); }
        void      init(const address_t& addr) override { m_impl.init(addr); }
        address_t find(rank_type rank) override { return m_impl.find(rank); }
    };

    std::unique_ptr<iface> m_impl;

    template<typename Impl>
    type_erased_address_db_t(Impl&& impl)
    : m_impl{std::make_unique<impl_t<std::remove_cv_t<std::remove_reference_t<Impl>>>>(
          std::forward<Impl>(impl))}
    {
    }

    inline rank_type rank() const { return m_impl->rank(); }
    inline rank_type size() const { return m_impl->size(); }
    inline int       est_size() const { return m_impl->est_size(); }
    inline void      init(const address_t& addr) { m_impl->init(addr); }
    inline address_t find(rank_type rank) { return m_impl->find(rank); }
};

} // namespace oomph
