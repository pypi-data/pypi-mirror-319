// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2024, Advanced Micro Devices, Inc. All rights reserved.

#include <iostream>
#include <numeric>
#include <initializer_list>
#include <cstdlib>

#include "profiler/profile_gemm_universal_reduce_impl.hpp"
#include "profiler_operation_registry.hpp"

enum struct GemmMatrixLayout
{
    MK_KN_MN, // 0
    MK_NK_MN, // 1
    KM_KN_MN, // 2
    KM_NK_MN, // 3
};

enum struct GemmDataType
{
    F32_F32_F32,    // 0
    F16_F16_F16,    // 1
    BF16_BF16_BF16, // 2
    INT8_INT8_INT8, // 3
    F8_F16_F16,     // 4
    BF16_I8_BF16,   // 5
    F16_F16_F16_F8, // 6
};

#define OP_NAME "gemm_universal_reduce"
#define OP_DESC "Universal GEMM"

int profile_gemm_universal_reduce(int argc, char* argv[])
{
    if(argc != 15 && argc != 18)
    {
        printf("arg1: tensor operation (" OP_NAME ": " OP_DESC ")\n");
        printf("arg2: data type (0: fp32; 1: fp16; 2: bf16; 3: int8; 4: f8@f16; 5: f16@i8; 6: f16, "
               "comp f8)\n");
        printf("arg3: matrix layout (0: A[m, k] * B[k, n] = C[m, n];\n");
        printf("arg4: verification (0: no; 1: yes)\n");
        printf("arg5: initialization (0: no init; 1: integer value; 2: decimal value)\n");
        printf("arg6: print tensor value (0: no; 1: yes)\n");
        printf("arg7: time kernel (0=no, 1=yes)\n");
        printf("arg8 to 13: M, N, K, StrideA, StrideB, StrideC\n");
        printf("arg14: split k into  mulitiple batch\n");
        printf("optional:\n");
        printf("arg15: number of warm-up cycles (default 1)\n");
        printf("arg16: number of iterations (default 10)\n");
        printf("arg17: memory for rotating buffer (default 0, size in MB)\n");
        exit(1);
    }

    const auto data_type       = static_cast<GemmDataType>(std::stoi(argv[2]));
    const auto layout          = static_cast<GemmMatrixLayout>(std::stoi(argv[3]));
    const bool do_verification = std::stoi(argv[4]);
    const int init_method      = std::stoi(argv[5]);
    const bool do_log          = std::stoi(argv[6]);
    const bool time_kernel     = std::stoi(argv[7]);

    const int M = std::stoi(argv[8]);
    const int N = std::stoi(argv[9]);
    const int K = std::stoi(argv[10]);

    const int StrideA = std::stoi(argv[11]);
    const int StrideB = std::stoi(argv[12]);
    const int StrideC = std::stoi(argv[13]);
    const int KBatch  = std::stoi(argv[14]);

    int n_warmup      = 1;
    int n_iter        = 10;
    uint64_t rotating = 0;
    if(argc == 18)
    {
        n_warmup = std::stoi(argv[15]);
        n_iter   = std::stoi(argv[16]);
        rotating = std::stoull(argv[17]) * 1024 * 1024;
    }

    using F32  = float;
    using F16  = ck::half_t;
    using BF16 = ck::bhalf_t;
    using I8   = int8_t;

    using Row = ck::tensor_layout::gemm::RowMajor;

    using DsDataType = ck::Tuple<>;
    using DsLayout   = ck::Tuple<>;

    auto profile = [&](auto a_type,
                       auto b_type,
                       auto acc_type,
                       auto c_type,
                       auto a_layout,
                       auto b_layout,
                       auto c_layout) {
        using ADataType   = decltype(a_type);
        using BDataType   = decltype(b_type);
        using AccDataType = decltype(acc_type);
        using CDataType   = decltype(c_type);

        using ALayout = decltype(a_layout);
        using BLayout = decltype(b_layout);
        using CLayout = decltype(c_layout);

        const int DefaultStrideA = ck::is_same_v<ALayout, Row> ? K : M;
        const int DefaultStrideB = ck::is_same_v<BLayout, Row> ? N : K;
        const int DefaultStrideC = ck::is_same_v<CLayout, Row> ? N : M;

        bool pass = ck::profiler::profile_gemm_universal_reduce_impl<ADataType,
                                                                     BDataType,
                                                                     DsDataType,
                                                                     AccDataType,
                                                                     CDataType,
                                                                     ALayout,
                                                                     BLayout,
                                                                     DsLayout,
                                                                     CLayout>(
            do_verification,
            init_method,
            do_log,
            time_kernel,
            M,
            N,
            K,
            (StrideA < 0) ? DefaultStrideA : StrideA,
            (StrideB < 0) ? DefaultStrideB : StrideB,
            (StrideC < 0) ? DefaultStrideC : StrideC,
            KBatch,
            n_warmup,
            n_iter,
            rotating);

        return pass ? 0 : 1;
    };

    if(data_type == GemmDataType::BF16_I8_BF16 && layout == GemmMatrixLayout::MK_KN_MN)
    {
        return profile(BF16{}, I8{}, F32{}, BF16{}, Row{}, Row{}, Row{});
    }
    else if(data_type == GemmDataType::BF16_BF16_BF16 && layout == GemmMatrixLayout::MK_KN_MN)
    {
        return profile(BF16{}, BF16{}, F32{}, BF16{}, Row{}, Row{}, Row{});
    }
    else if(data_type == GemmDataType::F16_F16_F16 && layout == GemmMatrixLayout::MK_KN_MN)
    {
        return profile(F16{}, F16{}, F32{}, F16{}, Row{}, Row{}, Row{});
    }
    else
    {
        std::cout << "this data_type & layout is not implemented" << std::endl;

        return 1;
    }
}

REGISTER_PROFILER_OPERATION(OP_NAME, OP_DESC, profile_gemm_universal_reduce);
