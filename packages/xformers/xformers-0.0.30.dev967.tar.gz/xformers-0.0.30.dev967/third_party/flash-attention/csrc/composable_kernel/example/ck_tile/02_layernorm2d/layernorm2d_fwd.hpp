// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2024, Advanced Micro Devices, Inc. All rights reserved.

#pragma once

#include "ck_tile/core.hpp"
#include "ck_tile/host/kernel_launch.hpp"
#include "ck_tile/ops/layernorm2d.hpp"
#include <string>

template <typename InType, typename OutType, typename XScaleDataType_, typename YScaleDataType_>
struct LayerNormTypeConfig;

template <typename OutType, typename XScaleDataType_, typename YScaleDataType_>
struct LayerNormTypeConfig<ck_tile::half_t, OutType, XScaleDataType_, YScaleDataType_>
{
    using XDataType       = ck_tile::half_t;
    using YDataType       = OutType;
    using GammaDataType   = ck_tile::half_t;
    using BetaDataType    = ck_tile::half_t;
    using MeanDataType    = ck_tile::half_t;
    using InvStdDataType  = ck_tile::half_t;
    using ComputeDataType = float;
    using XScaleDataType  = XScaleDataType_;
    using YScaleDataType  = YScaleDataType_;
};

template <typename OutType, typename XScaleDataType_, typename YScaleDataType_>
struct LayerNormTypeConfig<ck_tile::bf16_t, OutType, XScaleDataType_, YScaleDataType_>
{
    using XDataType       = ck_tile::bf16_t;
    using YDataType       = OutType;
    using GammaDataType   = ck_tile::bf16_t;
    using BetaDataType    = ck_tile::bf16_t;
    using MeanDataType    = ck_tile::bf16_t;
    using InvStdDataType  = ck_tile::bf16_t;
    using ComputeDataType = float;
    using XScaleDataType  = XScaleDataType_;
    using YScaleDataType  = YScaleDataType_;
};

// runtime args
struct layernorm2d_fwd_args : public ck_tile::Layernorm2dFwdHostArgs
{
};

// This is the public API, will be generated by script
struct layernorm2d_fwd_traits
{
    std::string prec_i; // input precision
    std::string prec_o; // output precision

    // if fused_quant == 1, need set prec_sx/prec_sy to proper string, otherwise can set
    // arbitrary(will skip check) if fused_quant == 2, need set prec_sy to proper string, otherwise
    // can set arbitrary(will skip check)
    std::string prec_sx; // x-scale, used for [1*N] input smooth quant
    std::string prec_sy; // y-scale, used for [M*1] output for next layer

    bool save_mean_var; //
    int fused_add;      // 0:no-add, 1:pre-add-store, 2:pre-add
    int fused_quant;    // 0:no-sweep, 1:smooth-dynamic-quant, 2:dynamic-quant
};

float layernorm2d_fwd(layernorm2d_fwd_traits, layernorm2d_fwd_args, const ck_tile::stream_config&);
