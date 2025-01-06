// SPDX-License-Identifier: MIT
// Copyright (c) 2018-2024, Advanced Micro Devices, Inc. All rights reserved.

#include <iomanip>
#include <vector>
#include <iostream>

#include "ck/ck.hpp"
#include "ck/tensor_operation/gpu/device/tensor_layout.hpp"
#include "ck/tensor_operation/gpu/device/device_normalization_bwd_data.hpp"
#include "ck/tensor_operation/gpu/element/element_wise_operation.hpp"

#include "ck/library/tensor_operation_instance/gpu/groupnorm_bwd_data.hpp"

using DYDataType         = float;
using XDataType          = float;
using GammaDataType      = float;
using MeanInvStdDataType = float;
using DXDataType         = float;

constexpr int Rank         = 5;
constexpr int NumReduceDim = 3;

struct SimpleDeviceMem
{
    SimpleDeviceMem() = delete;

    SimpleDeviceMem(std::size_t mem_size) : p_mem_{}
    {
        (void)hipMalloc(static_cast<void**>(&p_mem_), mem_size);
    }

    void* GetDeviceBuffer() { return p_mem_; }

    ~SimpleDeviceMem() { (void)hipFree(p_mem_); }

    void* p_mem_;
};

int main(int argc, char* argv[])
{
    ck::index_t N = 32;
    ck::index_t H = 16;
    ck::index_t W = 16;
    ck::index_t G = 64;
    ck::index_t C = 128;

    std::size_t length = N * H * W * G * C;

    std::vector<ck::index_t> strideDy = {H * W * G * C, W * G * C, G * C, C, 1};
    std::vector<ck::index_t> strideX  = strideDy;
    std::vector<ck::index_t> strideDx = strideDy;

    std::vector<ck::index_t> strideGamma      = {0, 0, 0, C, 1};
    std::vector<ck::index_t> strideMeanInvStd = {G, 0, 0, 1, 0};

    SimpleDeviceMem dy_dev(sizeof(DYDataType) * length);
    SimpleDeviceMem x_dev(sizeof(XDataType) * length);
    SimpleDeviceMem gamma_dev(sizeof(GammaDataType) * G * C);
    SimpleDeviceMem mean_dev(sizeof(MeanInvStdDataType) * N * G);
    SimpleDeviceMem inv_std_dev(sizeof(MeanInvStdDataType) * N * G);
    SimpleDeviceMem dx_dev(sizeof(DXDataType) * length);

    using DeviceOp = ck::tensor_operation::device::DeviceNormalizationBwdData<DYDataType,
                                                                              XDataType,
                                                                              GammaDataType,
                                                                              MeanInvStdDataType,
                                                                              DXDataType,
                                                                              Rank,
                                                                              NumReduceDim>;

    // get device op instances
    const auto op_ptrs = ck::tensor_operation::device::instance::DeviceOperationInstanceFactory<
        DeviceOp>::GetInstances();

    std::cout << "found " << op_ptrs.size() << " instances" << std::endl;

    std::string best_op_name;
    bool found            = false;
    int best_op_id        = -1;
    float best_ave_time   = std::numeric_limits<float>::max();
    float best_gb_per_sec = 0;

    // profile device operation instances
    std::cout << "Run all instances and do timing" << std::endl;

    for(int i = 0; i < op_ptrs.size(); ++i)
    {
        auto& op_ptr      = op_ptrs[i];
        auto argument_ptr = op_ptr->MakeArgumentPointer({N, H, W, G, C},
                                                        strideDy,
                                                        strideX,
                                                        strideGamma,
                                                        strideMeanInvStd,
                                                        strideMeanInvStd,
                                                        strideDx,
                                                        {1, 2, 4}, // reduceDims
                                                        dy_dev.GetDeviceBuffer(),
                                                        x_dev.GetDeviceBuffer(),
                                                        gamma_dev.GetDeviceBuffer(),
                                                        mean_dev.GetDeviceBuffer(),
                                                        inv_std_dev.GetDeviceBuffer(),
                                                        dx_dev.GetDeviceBuffer());

        auto invoker_ptr = op_ptr->MakeInvokerPointer();

        std::string op_name = op_ptr->GetTypeString();

        if(op_ptr->IsSupportedArgument(argument_ptr.get()))
        {
            size_t workspace_sz = op_ptr->GetWorkSpaceSize(argument_ptr.get());
            SimpleDeviceMem workspace(workspace_sz);
            op_ptr->SetWorkSpacePointer(argument_ptr.get(), workspace.GetDeviceBuffer());

            float ave_time = invoker_ptr->Run(argument_ptr.get(), StreamConfig{nullptr, true});

            std::size_t num_byte = sizeof(DYDataType) * length + sizeof(XDataType) * length +
                                   sizeof(GammaDataType) * G * C +
                                   sizeof(MeanInvStdDataType) * N * G * 2 +
                                   sizeof(DXDataType) * length;

            float gb_per_sec = num_byte / 1.E6 / ave_time;

            std::cout << "Perf: " << std::setw(10) << ave_time << " ms, " << gb_per_sec << " GB/s, "
                      << op_name << std::endl;

            if(ave_time < best_ave_time)
            {
                found           = true;
                best_op_id      = i;
                best_op_name    = op_name;
                best_ave_time   = ave_time;
                best_gb_per_sec = gb_per_sec;
            }
        }
        else
        {
            std::cout << op_name << " does not support this problem" << std::endl;
        }
    }

    // run the best intance
    if(found)
    {
        std::cout << "Best Perf: " << best_ave_time << " ms, " << best_gb_per_sec << " GB/s, "
                  << best_op_name << std::endl;

        auto& op_ptr = op_ptrs[best_op_id];
        std::cout << "Run the best instance without timing: " << op_ptr->GetTypeString()
                  << std::endl;

        auto argument_ptr = op_ptr->MakeArgumentPointer({N, H, W, G, C},
                                                        strideDy,
                                                        strideX,
                                                        strideGamma,
                                                        strideMeanInvStd,
                                                        strideMeanInvStd,
                                                        strideDx,
                                                        {1, 2, 4}, // reduceDims
                                                        dy_dev.GetDeviceBuffer(),
                                                        x_dev.GetDeviceBuffer(),
                                                        gamma_dev.GetDeviceBuffer(),
                                                        mean_dev.GetDeviceBuffer(),
                                                        inv_std_dev.GetDeviceBuffer(),
                                                        dx_dev.GetDeviceBuffer());

        auto invoker_ptr = op_ptr->MakeInvokerPointer();

        if(op_ptr->IsSupportedArgument(argument_ptr.get()))
        {
            size_t workspace_sz = op_ptr->GetWorkSpaceSize(argument_ptr.get());
            SimpleDeviceMem workspace(workspace_sz);
            op_ptr->SetWorkSpacePointer(argument_ptr.get(), workspace.GetDeviceBuffer());

            invoker_ptr->Run(argument_ptr.get(), StreamConfig{nullptr, false});
        }

        std::cout << "Done" << std::endl;
    }

    return 0;
}
