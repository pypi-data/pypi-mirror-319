// SPDX-License-Identifier: MIT
// Copyright (c) 2023-2024, Advanced Micro Devices, Inc. All rights reserved.

#include <tuple>

#include "ck/utility/data_type.hpp"
#include "ck/utility/tuple.hpp"

using InDataType  = ck::bhalf_t;
using WeiDataType = ck::bhalf_t;
using OutDataType = ck::bhalf_t;
// Use std tuple instead of ck tuple to avoid clang
// implicit instantiation of undefined template error.
using DDataTypes = std::tuple<ck::bhalf_t, ck::bhalf_t>;

#include "grouped_conv_fwd_scaleadd_scaleadd_relu.inc"

int main() { return execute_conv_fwd_scaleadd_scaleadd_relu(); }
