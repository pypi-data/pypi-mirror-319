/***************************************************************************************************
 * Copyright (c) 2017 - 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 **************************************************************************************************/

/**
  This example is almost the same as example 27 which uses 3xTF32 to run GEMM.  The only
  difference is that this example uses 3xtf32 on complex gemm.

  To enable this feature, the only change needs to make is to change OpMultiplyAddComplex
  to OpMultiplyAddComplexFastF32.
*/

#include <iostream>
#include <vector>
#include <limits>

#include "cutlass/cutlass.h"
#include "cutlass/gemm/device/gemm_complex.h"

#include "cutlass/util/command_line.h"
#include "cutlass/util/host_tensor.h"

#include "cutlass/util/reference/device/gemm_complex.h"
#include "cutlass/util/reference/host/tensor_reduce.h"
#include "cutlass/util/reference/host/tensor_compare.h"
#include "cutlass/util/reference/host/tensor_norm.h"
#include "cutlass/util/reference/host/tensor_copy.h"
#include "cutlass/util/reference/host/tensor_fill.h"
#include "cutlass/util/reference/host/error_metrics.h"
#include "cutlass/util/tensor_view_io.h"

#include "helper.h"

/////////////////////////////////////////////////////////////////////////////////////////////////

/// Result structure
struct Result {

  double runtime_ms;
  double gflops;
  cutlass::Status status;
  cudaError_t error;

  int m, n, k;
  double l2_norm_3xtf32_vs_fp64;
  double l2_norm_1xtf32_vs_fp64;
  double l2_norm_fp32_vs_fp64;

  // ctor
  Result(
    int m, int n, int k,
    double runtime_ms, double gflops,
    double l2_norm_3xtf32_vs_fp64,
    double l2_norm_1xtf32_vs_fp64,
    double l2_norm_fp32_vs_fp64) :
    m(m), n(n), k(k),
    runtime_ms(runtime_ms), gflops(gflops),
    l2_norm_3xtf32_vs_fp64(l2_norm_3xtf32_vs_fp64),
    l2_norm_1xtf32_vs_fp64(l2_norm_1xtf32_vs_fp64),
    l2_norm_fp32_vs_fp64(l2_norm_fp32_vs_fp64)   {}

  Result() {}

  //
  // Methods
  //
  static void print_csv_header() {
    std::cout << "M,N,K,Runtime(ms),GFLOPS,3xTF32_vs_FP64,1xTF32_vs_FP64,FP32_vs_FP64" << std::endl;
  }

  void print_csv_row() {
    std::cout << m << ","
              << n << ","
              << k << ","
              << runtime_ms << ","
              << gflops << ","
              << l2_norm_3xtf32_vs_fp64 << ","
              << l2_norm_1xtf32_vs_fp64 << ","
              << l2_norm_fp32_vs_fp64 << std::endl;
  }
};

std::vector<Result> results;

///////////////////////////////////////////////////////////////////////////////////////////////////

// Command line options parsing
struct Options {

  bool help;

  cutlass::gemm::GemmCoord problem_size;
  float alpha;
  float beta;
  std::string rand_mode;

  int iterations;
  int seed;
  bool benchmark;

  Options():
    help(false),
    problem_size({3456, 4096, 4096}),
    iterations(20),
    seed(1),
    alpha(1),
    beta(),
    rand_mode("uniform"),
    benchmark(false) { }

  bool valid() {
    return true;
  }

  // Parses the command line
  void parse(int argc, char const **args) {
    cutlass::CommandLine cmd(argc, args);

    if (cmd.check_cmd_line_flag("help")) {
      help = true;
    }

    cmd.get_cmd_line_argument("m", problem_size.m());
    cmd.get_cmd_line_argument("n", problem_size.n());
    cmd.get_cmd_line_argument("k", problem_size.k());

    cmd.get_cmd_line_argument("alpha", alpha);
    cmd.get_cmd_line_argument("beta", beta);

    cmd.get_cmd_line_argument("iterations", iterations);
    cmd.get_cmd_line_argument("seed", seed);
    cmd.get_cmd_line_argument("rand_mode", rand_mode);

    if (cmd.check_cmd_line_flag("benchmark")) {
      benchmark = true;
    }
  }

  /// Prints the usage statement.
  std::ostream & print_usage(std::ostream &out) const {

    out << "29_ampere_3xtf32_fast_accurate_tensorop_complex_gemm example\n\n"
      << "  This example uses the CUTLASS Library to emulate FP32 complex GEMM computations with TF32 tensor cores.\n\n"
      << "Options:\n\n"
      << "  --help                      If specified, displays this usage statement.\n\n"
      << "  --m=<int>                   GEMM M dimension\n"
      << "  --n=<int>                   GEMM N dimension\n"
      << "  --k=<int>                   GEMM K dimension\n"
      << "  --alpha=<f32>               Epilogue scalar alpha\n"
      << "  --beta=<f32>                Epilogue scalar beta\n\n"
      << "  --rand_mode=<string>        gauss / uniform*\n\n"
      << "  --seed=<int>                Random number seed (1*)\n\n"
      << "  --iterations=<int>          Number of profiling iterations to perform.\n\n"
      << "  --benchmark                 If set (true), performance benchmarking on several layers and batch-size.\n\n";

    out << "\n\nExamples:\n\n"
      << "$ ./examples/29_ampere_3xtf32_fast_accurate_tensorop_complex_gemm/29_3xtf32_complex_gemm --m=1024 --n=512 \\\n"
      << "     --alpha=2 --beta=0.707 \n\n";

    return out;
  }

  /// Compute performance in GFLOP/s
  double gflops(double runtime_s) const {

    // Number of real-valued multiply-adds
    int64_t fmas = problem_size.product();

    // Two flops per multiply-add
    return 2.0 * double(fmas) / double(1.0e9) / runtime_s;
  }
};

///////////////////////////////////////////////////////////////////////////////////////////////////

// The code section below describes matrix layout of input and output matrices. Column Major for
// Matrix A, Row Major for Matrix B and Row Major for Matrix C
using LayoutInputA = cutlass::layout::ColumnMajor;
using LayoutInputB = cutlass::layout::RowMajor;
using LayoutOutput = cutlass::layout::RowMajor;

// This code section describes whether you want to use tensor cores or regular SIMT cores on GPU SM
using MMAOp = cutlass::arch::OpClassTensorOp;

// This code section describes CUDA SM architecture number
using SmArch = cutlass::arch::Sm80;

// This code section describes the tile size a thread block will compute
using ShapeMMAThreadBlock =
    cutlass::gemm::GemmShape<64, 64, 16>;  // <- threadblock tile M = 128, N = 128, K = 16
// This code section describes tile size a warp will compute
using ShapeMMAWarp = cutlass::gemm::GemmShape<32, 32, 16>;  // <- warp tile M = 64, N = 64, K = 16
// This code section describes the size of MMA op
using ShapeMMAOp = cutlass::gemm::GemmShape<16, 8, 8>;  // <- MMA Op tile M = 16, N = 8, K = 8

// This code section describes how threadblocks are scheduled on GPU
using SwizzleThreadBlock = cutlass::gemm::threadblock::GemmIdentityThreadblockSwizzle<>;  // <- ??

// This code section describes the epilogue part of the kernel
using EpilogueOp = cutlass::epilogue::thread::LinearCombination<
    cutlass::complex<float>,                 // <- data type of output matrix
    1,                                       // <- the number of elements per vectorized
                                             //    memory access. For a byte, it's 16
                                             //    elements. This becomes the vector width of
                                             //    math instructions in the epilogue too
    cutlass::complex<float>,                 // <- data type of accumulator
    cutlass::complex<float>>;                 // <- data type for alpha/beta in linear combination function

// Number of pipelines you want to use
constexpr int NumStages = 3;
// Transform
constexpr cutlass::ComplexTransform TransformA = cutlass::ComplexTransform::kNone;
constexpr cutlass::ComplexTransform TransformB = cutlass::ComplexTransform::kNone;

//
// Gemm Operators (Gemm_3xTF32, Gemm_1xTF32, GEMM_F32, GEMM_F64)
//

// Gemm_3xTF32
using Gemm_3xTF32 = cutlass::gemm::device::GemmComplex<
                                              cutlass::complex<float>,
                                              LayoutInputA,
                                              cutlass::complex<float>,
                                              LayoutInputB,
                                              cutlass::complex<float>,
                                              LayoutOutput,
                                              cutlass::complex<float>,
                                              MMAOp,
                                              SmArch,
                                              ShapeMMAThreadBlock,
                                              ShapeMMAWarp,
                                              ShapeMMAOp,
                                              EpilogueOp,
                                              SwizzleThreadBlock,
                                              NumStages,
                                              TransformA,
                                              TransformB,
                                              cutlass::arch::OpMultiplyAddComplexFastF32>;

// Gemm_1xTF32
using Gemm_1xTF32 = cutlass::gemm::device::GemmComplex<
                                              cutlass::complex<float>,
                                              LayoutInputA,
                                              cutlass::complex<float>,
                                              LayoutInputB,
                                              cutlass::complex<float>,
                                              LayoutOutput,
                                              cutlass::complex<float>,
                                              MMAOp,
                                              SmArch,
                                              ShapeMMAThreadBlock,
                                              ShapeMMAWarp,
                                              ShapeMMAOp,
                                              EpilogueOp,
                                              SwizzleThreadBlock,
                                              NumStages,
                                              TransformA,
                                              TransformB,
                                              cutlass::arch::OpMultiplyAddComplex>;

bool run(Options &options) {

  // Create a tuple of problem size for matrix multiplication
  cutlass::gemm::GemmCoord problem_size = options.problem_size;

  ////////////////////////////////////////////////////////////////////////////////
  /// 1. Initialize F32 Precision input tensors using CUTLASS helper functions
  ////////////////////////////////////////////////////////////////////////////////
  cutlass::HostTensor<cutlass::complex<float>, LayoutInputA> tensor_a_F32(problem_size.mk());  // <- Create matrix A with dimensions M x K
  cutlass::HostTensor<cutlass::complex<float>, LayoutInputB> tensor_b_F32(problem_size.kn());  // <- Create matrix B with dimensions K x N
  cutlass::HostTensor<cutlass::complex<float>, LayoutOutput> tensor_c_F32(problem_size.mn());  // <- Create matrix C with dimensions M x N
  cutlass::HostTensor<cutlass::complex<float>, LayoutOutput> tensor_d_F32(problem_size.mn());  // <- Create matrix D with dimensions M x N

  if (options.rand_mode == "uniform") {
    const float min = -1;
    const float max =  1;
    // Fill input and output matrices on host using CUTLASS helper functions
    cutlass::reference::host::TensorFillRandomUniform(
        tensor_a_F32.host_view(),
        options.seed,
        double(max),
        double(min));      // <- Fill matrix A on host with uniform-distribution random data
    cutlass::reference::host::TensorFillRandomUniform(
        tensor_b_F32.host_view(),
        options.seed,
        double(max),
        double(min));      // <- Fill matrix B on host with uniform-distribution random data
    cutlass::reference::host::TensorFillRandomUniform(
        tensor_c_F32.host_view(),
        options.seed,
        double(max),
        double(min));      // <- Fill matrix C on host with uniform-distribution random data
  } else if (options.rand_mode == "gauss") {
    // Fill input and output matrices on host using CUTLASS helper functions
    cutlass::reference::host::TensorFillRandomGaussian(
        tensor_a_F32.host_view(),
        options.seed,
        double(0),
        double(5));      // <- Fill matrix A on host with gaussian-distribution random data
    cutlass::reference::host::TensorFillRandomGaussian(
        tensor_b_F32.host_view(),
        options.seed,
        double(0),
        double(5));      // <- Fill matrix B on host with gaussian-distribution random data
    cutlass::reference::host::TensorFillRandomGaussian(
        tensor_c_F32.host_view(),
        options.seed,
        double(0),
        double(5));      // <- Fill matrix C on host with gaussian-distribution random data
  }
  cutlass::reference::host::TensorFill(
      tensor_d_F32.host_view());  // <- fill matrix D on host with zeros

  // Copy data from host to GPU
  tensor_a_F32.sync_device();
  tensor_b_F32.sync_device();
  tensor_c_F32.sync_device();
  tensor_d_F32.sync_device();

  ////////////////////////////////////////////////////////////////////////////////
  /// 2. Initialize F64 tensors using the same values used for F32
  ////////////////////////////////////////////////////////////////////////////////
  // Gemm input operands (A, B, C)
  cutlass::HostTensor<cutlass::complex<double>, LayoutInputA> tensor_a_F64(problem_size.mk());  // <- Create matrix A with dimensions M x K
  cutlass::HostTensor<cutlass::complex<double>, LayoutInputB> tensor_b_F64(problem_size.kn());  // <- Create matrix B with dimensions K x N
  cutlass::HostTensor<cutlass::complex<double>, LayoutOutput> tensor_c_F64(problem_size.mn());  // <- Create matrix C with dimensions M x N

  // Gemm output (D) for GEMM_F64
  cutlass::HostTensor<cutlass::complex<double>, LayoutOutput> tensor_d_F64(problem_size.mn());  // <- Create matrix D with dimensions M x N
  // Gemm output (D) for GEMM_3xTF32
  cutlass::HostTensor<cutlass::complex<float>, LayoutOutput> tensor_d_3xTF32(problem_size.mn());  // <- Create matrix D with dimensions M x N
  // Gemm output (D) for GEMM_1xTF32
  cutlass::HostTensor<cutlass::complex<float>, LayoutOutput> tensor_d_1xTF32(problem_size.mn());  // <- Create matrix D with dimensions M x N

  // Copy values from the DP tensors
  cutlass::reference::host::TensorCopy(tensor_a_F64.host_view(), tensor_a_F32.host_view());
  cutlass::reference::host::TensorCopy(tensor_b_F64.host_view(), tensor_b_F32.host_view());
  cutlass::reference::host::TensorCopy(tensor_c_F64.host_view(), tensor_c_F32.host_view());
  cutlass::reference::host::TensorCopy(tensor_d_F64.host_view(), tensor_d_F32.host_view());
  cutlass::reference::host::TensorCopy(tensor_d_3xTF32.host_view(), tensor_d_F32.host_view());
  cutlass::reference::host::TensorCopy(tensor_d_1xTF32.host_view(), tensor_d_F32.host_view());

  // Copy data from host to GPU
  tensor_a_F64.sync_device();
  tensor_b_F64.sync_device();
  tensor_c_F64.sync_device();
  tensor_d_F64.sync_device();
  tensor_d_3xTF32.sync_device();
  tensor_d_1xTF32.sync_device();

  // Initialize alpha and beta for dot product computation
  cutlass::complex<float> alpha = cutlass::complex<float>(options.alpha);
  cutlass::complex<float> beta =  cutlass::complex<float>(options.beta);

  // Split K dimension into 1 partitions
  int split_k_slices = 1;

  ////////////////////////////////////////////////////////////////////////////////
  /// 3. Run  3xTF32 kernel within a profiling loop
  ////////////////////////////////////////////////////////////////////////////////
  // Create a tuple of gemm kernel arguments. This is later passed as arguments to launch
  // instantiated CUTLASS kernel
  typename Gemm_3xTF32::Arguments arguments_3xtf32{problem_size,  // <- problem size of matrix multiplication
                                     tensor_a_F32.device_ref(),  // <- reference to matrix A on device
                                     tensor_b_F32.device_ref(),  // <- reference to matrix B on device
                                     tensor_c_F32.device_ref(),  // <- reference to matrix C on device
                                     tensor_d_3xTF32.device_ref(),  // <- reference to matrix D on device
                                     {alpha, beta},          // <- tuple of alpha and beta
                                     split_k_slices};        // <- k-dimension split factor

  // Using the arguments, query for extra workspace required for matrix multiplication computation
  size_t workspace_size_3xtf32 = Gemm_3xTF32::get_workspace_size(arguments_3xtf32);

  // Allocate workspace memory
  cutlass::device_memory::allocation<uint8_t> workspace_3xtf32(workspace_size_3xtf32);

  // Instantiate CUTLASS kernel depending on templates
  Gemm_3xTF32 gemm_op;

  // Check the problem size is supported or not
  cutlass::Status status_3xtf32 = gemm_op.can_implement(arguments_3xtf32);
  CUTLASS_CHECK(status_3xtf32);

  // Initialize CUTLASS kernel with arguments and workspace pointer
  status_3xtf32 = gemm_op.initialize(arguments_3xtf32, workspace_3xtf32.get());
  CUTLASS_CHECK(status_3xtf32);

  // Result structure
  Result result;

  //
  // Construct events
  //

  cudaEvent_t events[2];

  for (auto & event : events) {
    result.error = cudaEventCreate(&event);
    if (result.error != cudaSuccess) {
      std::cerr << "cudaEventCreate() failed: " << cudaGetErrorString(result.error) << std::endl;
      return false;
    }
  }

  // Record an event at the start of a series of GEMMs
  result.error = cudaEventRecord(events[0]);
  if (result.error != cudaSuccess) {
    std::cerr << "cudaEventRecord() failed: " << cudaGetErrorString(result.error) << std::endl;
    return false;
  }

  //
  // Run profiling loop
  //

  for (int iter = 0; iter < options.iterations; ++iter) {
    // Launch initialized CUTLASS kernel
    status_3xtf32 = gemm_op();
    CUTLASS_CHECK(status_3xtf32);
  }

  //
  // Stop profiling loop
  //

  // Record an event when the GEMMs are complete
  result.error = cudaEventRecord(events[1]);
  if (result.error != cudaSuccess) {
    std::cerr << "cudaEventRecord() failed: " << cudaGetErrorString(result.error) << std::endl;
    return false;
  }

  // Wait for work on the device to complete.
  result.error = cudaEventSynchronize(events[1]);
  if (result.error != cudaSuccess) {
    std::cerr << "cudaEventSynchronize() failed: " << cudaGetErrorString(result.error) << std::endl;
    return false;
  }

  // Measure elapsed runtime
  float runtime_ms = 0;
  result.error = cudaEventElapsedTime(&runtime_ms, events[0], events[1]);
  if (result.error != cudaSuccess) {
    std::cerr << "cudaEventElapsed() failed: " << cudaGetErrorString(result.error) << std::endl;
    return false;
  }

  // Compute average runtime and GFLOPs.
  result.m = problem_size.m();
  result.n = problem_size.n();
  result.k = problem_size.k();
  result.runtime_ms = double(runtime_ms) / double(options.iterations);
  result.gflops = options.gflops(result.runtime_ms / 1000.0);

  // Cleanup
  for (auto event : events) {
    (void)cudaEventDestroy(event);
  }

  tensor_d_3xTF32.sync_host();

  ////////////////////////////////////////////////////////////////////////////////
  /// 4. Run TF32 kernel without profiling loop
  ////////////////////////////////////////////////////////////////////////////////
  // Create a tuple of gemm kernel arguments. This is later passed as arguments to launch
  // instantiated CUTLASS kernel
  typename Gemm_1xTF32::Arguments arguments_1xtf32{problem_size,  // <- problem size of matrix multiplication
                                          tensor_a_F32.device_ref(),  // <- reference to matrix A on device
                                          tensor_b_F32.device_ref(),  // <- reference to matrix B on device
                                          tensor_c_F32.device_ref(),  // <- reference to matrix C on device
                                          tensor_d_1xTF32.device_ref(),  // <- reference to matrix D on device
                                          {alpha, beta},          // <- tuple of alpha and beta
                                          split_k_slices};        // <- k-dimension split factor

  // Using the arguments, query for extra workspace required for matrix multiplication computation
  size_t workspace_size_1xtf32 = Gemm_1xTF32::get_workspace_size(arguments_1xtf32);

  // Allocate workspace memory
  cutlass::device_memory::allocation<uint8_t> workspace_1xtf32(workspace_size_1xtf32);

  // Instantiate CUTLASS kernel depending on templates
  Gemm_1xTF32 gemm_op_1xtf32;

  // Check the problem size is supported or not
  cutlass::Status status_1xtf32 = gemm_op_1xtf32.can_implement(arguments_1xtf32);
  CUTLASS_CHECK(status_1xtf32);

  // Initialize CUTLASS kernel with arguments and workspace pointer
  status_1xtf32 = gemm_op_1xtf32.initialize(arguments_1xtf32, workspace_1xtf32.get());
  CUTLASS_CHECK(status_1xtf32);

  // Launch initialized CUTLASS kernel
  status_1xtf32 = gemm_op_1xtf32();
  CUTLASS_CHECK(status_1xtf32);

  tensor_d_1xTF32.sync_host();

  ////////////////////////////////////////////////////////////////////////////////
  // Run reference kernel (F64)
  ////////////////////////////////////////////////////////////////////////////////

  // Launch device reference gemm kernel
  cutlass::reference::device::GemmComplex(
                   problem_size,
                   alpha,
                   tensor_a_F64.device_ref(),
                   TransformA,
                   tensor_b_F64.device_ref(),
                   TransformB,
                   beta,
                   tensor_c_F64.device_ref(),
                   tensor_d_F64.device_ref(),
                   cutlass::complex<double>(0.f));

  // Wait for kernels to finish
  cudaDeviceSynchronize();

  // Copy output data from CUTLASS and reference kernel to host for comparison
  tensor_d_F64.sync_host();

  ////////////////////////////////////////////////////////////////////////////////
  // Run reference kernel (F32)
  ////////////////////////////////////////////////////////////////////////////////

  // Launch device reference gemm kernel
  cutlass::reference::device::GemmComplex(
                   problem_size,
                   alpha,
                   tensor_a_F32.device_ref(),
                   TransformA,
                   tensor_b_F32.device_ref(),
                   TransformB,
                   beta,
                   tensor_c_F32.device_ref(),
                   tensor_d_F32.device_ref(),
                   cutlass::complex<float>(0.f));

  // Wait for kernels to finish
  cudaDeviceSynchronize();

  // Copy output data from CUTLASS and reference kernel to host for comparison
  tensor_d_F32.sync_host();

  ////////////////////////////////////////////////////////////////////////////////
  ///////               Compute l2 norms
  ////////////////////////////////////////////////////////////////////////////////

  // l2 norm 3xTF32 vs F64
  cutlass::HostTensor<cutlass::complex<double>, LayoutOutput> tensor_d_3xTF32_in_F64(problem_size.mn());
  cutlass::reference::host::TensorCopy(tensor_d_3xTF32_in_F64.host_view(), tensor_d_3xTF32.host_view());

  result.l2_norm_3xtf32_vs_fp64 = cutlass::reference::host::TensorRelativeErrorMetric(
    tensor_d_3xTF32_in_F64.host_view(), tensor_d_F64.host_view());

  // l2 norm 1xTF32 vs F64
  cutlass::HostTensor<cutlass::complex<double>, LayoutOutput> tensor_d_1xTF32_in_F64(problem_size.mn());
  cutlass::reference::host::TensorCopy(tensor_d_1xTF32_in_F64.host_view(), tensor_d_1xTF32.host_view());

  result.l2_norm_1xtf32_vs_fp64 = cutlass::reference::host::TensorRelativeErrorMetric(
    tensor_d_1xTF32_in_F64.host_view(), tensor_d_F64.host_view());

  // l2 norm F32 vs F64
  cutlass::HostTensor<cutlass::complex<double>, LayoutOutput> tensor_d_F32_in_F64(problem_size.mn());
  cutlass::reference::host::TensorCopy(tensor_d_F32_in_F64.host_view(), tensor_d_F32.host_view());

  result.l2_norm_fp32_vs_fp64 = cutlass::reference::host::TensorRelativeErrorMetric(
    tensor_d_F32_in_F64.host_view(), tensor_d_F64.host_view());

  results.push_back(result);

  ///////////////////////////////////////////////////////////////////////////////

  // Check if output from CUTLASS kernel and reference kernel are equal or not

  std::cout << std::fixed;
  std::cout.precision(4);
  std::cout << "Runtime: " << result.runtime_ms << " ms" << std::endl;
  std::cout.precision(2);
  std::cout << "GFLOPs: " << result.gflops << std::endl;
  std::cout << "Normalized L2 norm of" << std::endl;
  std::cout.precision(8);
  std::cout << std::scientific
            << " - 3xTF32 error with FP64 reference : " << result.l2_norm_3xtf32_vs_fp64 << std::endl
            << " - 1xTF32 error with FP64 reference : " << result.l2_norm_1xtf32_vs_fp64 << std::endl
            << " - FP32 error with FP64 reference   : " << result.l2_norm_fp32_vs_fp64 << std::endl;

  return true;
}

int main(int argc, const char **argv) {

  bool notSupported = false;

  // Ampere Tensor Core operations exposed with mma.sync and ldmatrix are first available
  // in CUDA 11.0.
  //
  // CUTLASS must be compiled with CUDA 11.0 Toolkit to run these examples.
  if (!(__CUDACC_VER_MAJOR__ >= 11)) {
    std::cerr << "Ampere Tensor Core operations must be compiled with CUDA 11.0 Toolkit or later." << std::endl;
    notSupported = true;
  }

  cudaDeviceProp props;

  cudaError_t error = cudaGetDeviceProperties(&props, 0);
  if (error != cudaSuccess) {
    std::cerr << "cudaGetDeviceProperties() returned an error: " << cudaGetErrorString(error) << std::endl;
    return -1;
  }

  if (!((props.major * 10 + props.minor) >= 80)) {
    std::cerr << "Ampere Tensor Core operations must be run on a machine with compute capability at least 80."
              << std::endl;
    notSupported = true;
  }

  if (notSupported) {
    // Returning zero so this test passes on older Toolkits. Its actions are no-op.
    return 0;
  }

  Options options;
  options.parse(argc, argv);

  if (options.help) {
    options.print_usage(std::cout) << std::endl;
    return 0;
  }

  bool result = true;

  if (options.benchmark) {
    for (int k = 4; k <= 65536; k *= 2) {

      options.problem_size[2] = k;

      printf("Gemm problem size: %d x %d x %d\n", \
        options.problem_size.m(), options.problem_size.n(), options.problem_size.k());

      if (!options.valid()) {
        std::cerr << "Invalid problem." << std::endl;
        return -1;
      }

      result &= run(options);
    }
  } else {
    // Execute one problem size
    if (!options.valid()) {
      std::cerr << "Invalid problem." << std::endl;
      return -1;
    }

    result = run(options);
  }

  if (!result) return -1;

  std::cout << std::endl << "CSV results" << std::endl;
  Result::print_csv_header();
  for(auto &r : results)
    r.print_csv_row();

  return 0;
}
