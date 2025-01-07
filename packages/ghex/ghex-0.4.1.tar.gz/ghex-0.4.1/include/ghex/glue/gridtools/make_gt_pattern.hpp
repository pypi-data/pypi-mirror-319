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

#include <ghex/structured/pattern.hpp>
#include <ghex/structured/regular/halo_generator.hpp>
#include <array>

namespace ghex
{
template<typename Grid, typename Halos>
auto
make_gt_pattern(Grid& grid, Halos&& halos)
{
    const std::array<int, 3> first{0, 0, 0};
    const std::array<int, 3> last{
        grid.m_global_extents[0] - 1, grid.m_global_extents[1] - 1, grid.m_global_extents[2] - 1};
    using halo_gen_type = structured::regular::halo_generator<typename Grid::domain_id_type,
        std::integral_constant<int, 3>>;
    auto halo_gen = halo_gen_type(first, last, std::forward<Halos>(halos), grid.m_periodic);

    return make_pattern<structured::grid>(grid.m_context, halo_gen, grid.m_domains);
}

} // namespace ghex
