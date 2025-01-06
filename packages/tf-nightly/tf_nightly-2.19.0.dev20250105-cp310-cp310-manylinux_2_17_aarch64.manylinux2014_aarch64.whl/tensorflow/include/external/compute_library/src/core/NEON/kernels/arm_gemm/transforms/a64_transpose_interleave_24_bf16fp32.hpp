/*
 * Copyright (c) 2021, 2023 Arm Limited.
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
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#pragma once

#ifdef __aarch64__

namespace {

void a64_transpose_interleave_24_bf16fp32(float *out, const bfloat16 *in, size_t width, size_t in_stride, size_t height)
{
    size_t out_stride = 12 * height * sizeof(float);

    __asm__ __volatile__(
      "cmp %x[height], #0x4\n"
      "blt 10f\n"
      "1:"  // Main row loop: Head
      "mov x25, %x[in]\n"
      "mov x24, %x[width]\n"
      "add x23, x25, %x[in_stride]\n"
      "add x22, x23, %x[in_stride]\n"
      "add x20, x22, %x[in_stride]\n"
      "cmp x24, #0x18\n"
      "add %x[in], x20, %x[in_stride]\n"
      "mov x21, %x[out]\n"
      "sub %x[height], %x[height], #0x4\n"
      "blt 3f\n"
      "2:"  // Main row loop: Unroll column loop
      "ldr q18, [x25], #0x10\n"
      "ldr q17, [x23], #0x10\n"
      "sub x24, x24, #0x18\n"
      "shll v26.4s, v18.4h, #0x10\n"
      "ldr q16, [x22], #0x10\n"
      "ldr q25, [x20], #0x10\n"
      "shll2 v24.4s, v18.8h, #0x10\n"
      "shll v5.4s, v17.4h, #0x10\n"
      "ldr q23, [x25], #0x10\n"
      "ldr q22, [x23], #0x10\n"
      "shll v21.4s, v23.4h, #0x10\n"
      "shll2 v4.4s, v17.8h, #0x10\n"
      "ldr q20, [x22], #0x10\n"
      "ldr q3, [x20], #0x10\n"
      "shll v2.4s, v22.4h, #0x10\n"
      "shll v1.4s, v16.4h, #0x10\n"
      "ldr q19, [x25], #0x10\n"
      "ldr q18, [x23], #0x10\n"
      "shll2 v0.4s, v16.8h, #0x10\n"
      "shll v31.4s, v20.4h, #0x10\n"
      "ldr q17, [x22], #0x10\n"
      "ldr q16, [x20], #0x10\n"
      "shll v30.4s, v25.4h, #0x10\n"
      "shll2 v29.4s, v25.8h, #0x10\n"
      "shll v28.4s, v3.4h, #0x10\n"
      "str q26, [x21, #0x0]\n"
      "cmp x24, #0x18\n"
      "shll2 v27.4s, v23.8h, #0x10\n"
      "str q24, [x21, #0x10]\n"
      "shll v26.4s, v19.4h, #0x10\n"
      "shll2 v25.4s, v19.8h, #0x10\n"
      "str q21, [x21, #0x20]\n"
      "shll2 v24.4s, v22.8h, #0x10\n"
      "shll v23.4s, v18.4h, #0x10\n"
      "str q5, [x21, #0x30]\n"
      "shll2 v22.4s, v18.8h, #0x10\n"
      "shll2 v21.4s, v20.8h, #0x10\n"
      "str q4, [x21, #0x40]\n"
      "shll v20.4s, v17.4h, #0x10\n"
      "shll2 v19.4s, v17.8h, #0x10\n"
      "str q2, [x21, #0x50]\n"
      "shll2 v18.4s, v3.8h, #0x10\n"
      "shll v17.4s, v16.4h, #0x10\n"
      "str q1, [x21, #0x60]\n"
      "shll2 v16.4s, v16.8h, #0x10\n"
      "str q0, [x21, #0x70]\n"
      "str q31, [x21, #0x80]\n"
      "str q30, [x21, #0x90]\n"
      "str q29, [x21, #0xa0]\n"
      "str q28, [x21, #0xb0]\n"
      "add x21, x21, %x[out_stride]\n"
      "str q27, [x21, #0x0]\n"
      "str q26, [x21, #0x10]\n"
      "str q25, [x21, #0x20]\n"
      "str q24, [x21, #0x30]\n"
      "str q23, [x21, #0x40]\n"
      "str q22, [x21, #0x50]\n"
      "str q21, [x21, #0x60]\n"
      "str q20, [x21, #0x70]\n"
      "str q19, [x21, #0x80]\n"
      "str q18, [x21, #0x90]\n"
      "str q17, [x21, #0xa0]\n"
      "str q16, [x21, #0xb0]\n"
      "add x21, x21, %x[out_stride]\n"
      "bge 2b\n"
      "3:"  // Main row loop: Unroll column loop skip
      "cmp x24, #0xc\n"
      "blt 5f\n"
      "4:"  // Main row loop: Column loop
      "ldr q16, [x25], #0x10\n"
      "ldr q21, [x23], #0x10\n"
      "sub x24, x24, #0xc\n"
      "cmp x24, #0xc\n"
      "ldr q20, [x22], #0x10\n"
      "ldr q27, [x20], #0x10\n"
      "shll v19.4s, v16.4h, #0x10\n"
      "shll2 v26.4s, v16.8h, #0x10\n"
      "ldr d16, [x25], #0x8\n"
      "ldr d18, [x23], #0x8\n"
      "shll v25.4s, v16.4h, #0x10\n"
      "shll v24.4s, v21.4h, #0x10\n"
      "ldr d17, [x22], #0x8\n"
      "ldr d16, [x20], #0x8\n"
      "shll2 v23.4s, v21.8h, #0x10\n"
      "shll v22.4s, v18.4h, #0x10\n"
      "shll v21.4s, v20.4h, #0x10\n"
      "shll2 v20.4s, v20.8h, #0x10\n"
      "str q19, [x21, #0x0]\n"
      "shll v19.4s, v17.4h, #0x10\n"
      "shll v18.4s, v27.4h, #0x10\n"
      "str q26, [x21, #0x10]\n"
      "shll2 v17.4s, v27.8h, #0x10\n"
      "shll v16.4s, v16.4h, #0x10\n"
      "str q25, [x21, #0x20]\n"
      "str q24, [x21, #0x30]\n"
      "str q23, [x21, #0x40]\n"
      "str q22, [x21, #0x50]\n"
      "str q21, [x21, #0x60]\n"
      "str q20, [x21, #0x70]\n"
      "str q19, [x21, #0x80]\n"
      "str q18, [x21, #0x90]\n"
      "str q17, [x21, #0xa0]\n"
      "str q16, [x21, #0xb0]\n"
      "add x21, x21, %x[out_stride]\n"
      "bge 4b\n"
      "5:"  // Main row loop: Column loop skip
      "cmp x24, #0x4\n"
      "blt 7f\n"
      "6:"  // Main row loop: width 4 loop: loop
      "ldr d19, [x25], #0x8\n"
      "ldr d18, [x23], #0x8\n"
      "sub x24, x24, #0x4\n"
      "cmp x24, #0x4\n"
      "ldr d17, [x22], #0x8\n"
      "ldr d16, [x20], #0x8\n"
      "shll v19.4s, v19.4h, #0x10\n"
      "shll v18.4s, v18.4h, #0x10\n"
      "shll v17.4s, v17.4h, #0x10\n"
      "shll v16.4s, v16.4h, #0x10\n"
      "str q19, [x21, #0x0]\n"
      "str q18, [x21, #0x30]\n"
      "str q17, [x21, #0x60]\n"
      "str q16, [x21, #0x90]\n"
      "add x21, x21, #0x10\n"
      "bge 6b\n"
      "7:"  // Main row loop: width 4 loop: skip
      "cmp x24, #0x1\n"
      "blt 9f\n"
      "8:"  // Main row loop: width 1 loop: loop
      "ldr h19, [x25], #0x2\n"
      "ldr h18, [x23], #0x2\n"
      "sub x24, x24, #0x1\n"
      "cmp x24, #0x1\n"
      "ldr h17, [x22], #0x2\n"
      "ldr h16, [x20], #0x2\n"
      "shll v19.4s, v19.4h, #0x10\n"
      "shll v18.4s, v18.4h, #0x10\n"
      "shll v17.4s, v17.4h, #0x10\n"
      "shll v16.4s, v16.4h, #0x10\n"
      "str s19, [x21, #0x0]\n"
      "str s18, [x21, #0x30]\n"
      "str s17, [x21, #0x60]\n"
      "str s16, [x21, #0x90]\n"
      "add x21, x21, #0x4\n"
      "bge 8b\n"
      "9:"  // Main row loop: width 1 loop: skip
      "cmp %x[height], #0x4\n"
      "add %x[out], %x[out], #0xc0\n"
      "bge 1b\n"
      "cbz %x[height], 20f\n"
      "10:"  // Main loop skip

      "11:"  // Tail row loop: Head
      "mov x20, %x[width]\n"
      "mov x25, %x[in]\n"
      "cmp x20, #0x18\n"
      "add %x[in], x25, %x[in_stride]\n"
      "mov x21, %x[out]\n"
      "sub %x[height], %x[height], #0x1\n"
      "blt 13f\n"
      "12:"  // Tail row loop: Unroll column loop
      "ldr q16, [x25], #0x10\n"
      "ldr q20, [x25], #0x10\n"
      "sub x20, x20, #0x18\n"
      "shll v18.4s, v16.4h, #0x10\n"
      "ldr q19, [x25], #0x10\n"
      "shll2 v17.4s, v16.8h, #0x10\n"
      "shll v16.4s, v20.4h, #0x10\n"
      "str q18, [x21, #0x0]\n"
      "str q17, [x21, #0x10]\n"
      "cmp x20, #0x18\n"
      "shll2 v18.4s, v20.8h, #0x10\n"
      "shll v17.4s, v19.4h, #0x10\n"
      "str q16, [x21, #0x20]\n"
      "add x21, x21, %x[out_stride]\n"
      "shll2 v16.4s, v19.8h, #0x10\n"
      "str q18, [x21, #0x0]\n"
      "str q17, [x21, #0x10]\n"
      "str q16, [x21, #0x20]\n"
      "add x21, x21, %x[out_stride]\n"
      "bge 12b\n"
      "13:"  // Tail row loop: Unroll column loop skip
      "cmp x20, #0xc\n"
      "blt 15f\n"
      "14:"  // Tail row loop: Column loop
      "ldr q17, [x25], #0x10\n"
      "ldr d18, [x25], #0x8\n"
      "sub x20, x20, #0xc\n"
      "cmp x20, #0xc\n"
      "shll v16.4s, v17.4h, #0x10\n"
      "shll2 v17.4s, v17.8h, #0x10\n"
      "str q16, [x21, #0x0]\n"
      "shll v16.4s, v18.4h, #0x10\n"
      "str q17, [x21, #0x10]\n"
      "str q16, [x21, #0x20]\n"
      "add x21, x21, %x[out_stride]\n"
      "bge 14b\n"
      "15:"  // Tail row loop: Column loop skip
      "cmp x20, #0x4\n"
      "blt 17f\n"
      "16:"  // Tail row loop: width 4 loop: loop
      "ldr d16, [x25], #0x8\n"
      "sub x20, x20, #0x4\n"
      "cmp x20, #0x4\n"
      "shll v16.4s, v16.4h, #0x10\n"
      "str q16, [x21, #0x0]\n"
      "add x21, x21, #0x10\n"
      "bge 16b\n"
      "17:"  // Tail row loop: width 4 loop: skip
      "cmp x20, #0x1\n"
      "blt 19f\n"
      "18:"  // Tail row loop: width 1 loop: loop
      "ldr h16, [x25], #0x2\n"
      "sub x20, x20, #0x1\n"
      "cmp x20, #0x1\n"
      "shll v16.4s, v16.4h, #0x10\n"
      "str s16, [x21, #0x0]\n"
      "add x21, x21, #0x4\n"
      "bge 18b\n"
      "19:"  // Tail row loop: width 1 loop: skip
      "cmp %x[height], #0x1\n"
      "add %x[out], %x[out], #0x30\n"
      "bge 11b\n"
      "20:"  // Done

      : [height] "+&r" (height), [in] "+&r" (in), [out] "+&r" (out)
      : [in_stride] "r" (in_stride), [out_stride] "r" (out_stride), [width] "r" (width)
      : "cc", "memory", "v0", "v1", "v2", "v3", "v4", "v5", "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", "v28", "v29", "v30", "v31", "x20", "x21", "x22", "x23", "x24", "x25"
    );
}

} // anonymous namespace
template<>
void Transform<12, 1, true, VLType::None>(
    float *out, const bfloat16 *in, int stride, int x0, int xmax, int k0, int kmax)
{
    a64_transpose_interleave_24_bf16fp32(
        out,
        in + k0 * stride + x0,
        (xmax-x0),
        stride * sizeof(bfloat16),
        (kmax-k0)
    );
}

#endif
