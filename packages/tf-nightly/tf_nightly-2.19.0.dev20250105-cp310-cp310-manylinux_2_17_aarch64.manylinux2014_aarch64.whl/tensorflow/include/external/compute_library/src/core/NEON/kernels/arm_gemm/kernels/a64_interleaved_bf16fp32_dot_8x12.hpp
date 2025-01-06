/*
 * Copyright (c) 2019-2021 Arm Limited.
 *
 * SPDX-License-Identifier: MIT
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */
#pragma once

#ifdef __aarch64__
#include "../std_transforms_fixed.hpp"
#include "../bfloat.hpp"
#include "../performance_parameters.hpp"

#define ARGLIST  \
    const bfloat16 *, const bfloat16 *, \
    float *, int, int, int

namespace arm_gemm
{
// Actual kernel implementations
void a64_interleaved_bf16fp32_dot_8x12( ARGLIST );

class cls_a64_interleaved_bf16fp32_dot_8x12
{
public:
    typedef bfloat16 operand_type;
    typedef float result_type;

    typedef void (*kern_type)( ARGLIST );

    /* Kernel blocking parameters */
    static constexpr unsigned int out_height()
    {
        return 8;
    }

    static unsigned int out_width()
    {
        return 12;
    }

    static unsigned int stripe_width()
    {
        return 4;
    }

    static constexpr unsigned int k_unroll()
    {
        return 2;
    }


    StdTransformsFixed<operand_type, result_type, 8, 12, 2> transforms = {};
    StdTransformsFixed<operand_type, result_type, 8, 12, 2, true> transforms_quantized = {};
    template<typename T>
    static inline PerformanceParameters get_performance_parameters(const CPUInfo *ci)
    {

        if (std::is_same<T, bfloat16>::value) {
            switch (ci->get_cpu_model()) {
                default:
                    return { 15.93, 4.16, 7.19 };
                case CPUModel::V1:
                    return { 20.88, 5.10, 6.57 };
                case CPUModel::A510:
                    return { 7.77, 3.69, 3.02 };
            }
        }

        return { 1.0 };
    }

    // Default to the generic kernel
    kern_type kernel=a64_interleaved_bf16fp32_dot_8x12;
    cls_a64_interleaved_bf16fp32_dot_8x12(const CPUInfo *)
    {
    }
};

} // namespace arm_gemm

#undef ARGLIST

#endif // __aarch64__
