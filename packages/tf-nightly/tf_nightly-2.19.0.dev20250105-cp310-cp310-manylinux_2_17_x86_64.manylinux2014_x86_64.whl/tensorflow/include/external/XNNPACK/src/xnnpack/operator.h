// Copyright (c) Facebook, Inc. and its affiliates.
// All rights reserved.
//
// Copyright 2019 Google LLC
//
// This source code is licensed under the BSD-style license found in the
// LICENSE file in the root directory of this source tree.

#pragma once

#include <stddef.h>
#include <stdint.h>

#include "xnnpack.h"
#include "xnnpack/common.h"
#include "xnnpack/compute.h"
#include "xnnpack/microfnptr.h"
#include "xnnpack/microkernel-type.h"
#include "xnnpack/microparams.h"
#include "xnnpack/operator-type.h"
#include "pthreadpool.h"

// Maximum number of pthreadpool parallelization invocations per operator.
#define XNN_MAX_COMPUTE_INVOCATIONS 3

#ifdef __cplusplus
extern "C" {
#endif

struct xnn_ukernel_conv2d {
  union {
    xnn_conv_hwc2chw_ukernel_fn hwc2chw_fn;
    xnn_conv_hwc_ukernel_fn hwc_fn;
  };
  uint8_t output_height_tile;
  uint8_t output_channel_tile;
};

struct xnn_ukernel_dwconv {
  union {
    xnn_dwconv_unipass_ukernel_fn unipass_fn;
    xnn_dwconv_multipass_ukernel_fn multipass_fn;
  };
  uint8_t primary_tile;
  uint8_t middle_tile;
  uint8_t last_tile;
  // For unipass, tile_size == primary_tile, otherwise it is calculated based on
  // how many pass the middle_tile runs.
  size_t tile_size;
};

// Direct 2D Depthwise Convolution
struct xnn_ukernel_dwconv2d {
  union {
    xnn_dwconv2d_chw_ukernel_fn chw_fn;
  };
  uint8_t output_width_tile;
};

struct xnn_ukernel_gemm {
  struct xnn_hmp_gemm_ukernel gemm_cases[XNN_MAX_MR];
  // Attention operator uses both types of packing.
  xnn_packw_gemm_goi_ukernel_fn packw_gemm_goi;
  xnn_packw_gemm_gio_ukernel_fn packw_gemm_gio;
  uint8_t mr;
  uint8_t mr_packed;
  uint8_t nr;
  uint8_t kr;
  uint8_t sr;
  uint8_t kp;
};

struct xnn_ukernel_igemm {
  struct xnn_hmp_igemm_ukernel igemm_cases[XNN_MAX_MR];
  struct xnn_hmp_gemm_ukernel gemm_cases[XNN_MAX_MR];
  uint8_t mr;
  uint8_t nr;
  uint8_t kr;
  uint8_t sr;
};

struct xnn_ukernel_spmm {
  xnn_spmm_ukernel_fn function;
  uint8_t mr;
};

struct xnn_ukernel_vmulcaddc {
  xnn_vmulcaddc_ukernel_fn function;
  uint8_t mr;
};

struct xnn_ukernel_vbinary {
  xnn_vbinary_ukernel_fn op_fn;
  xnn_vbinary_ukernel_fn opc_fn;
  xnn_vbinary_ukernel_fn ropc_fn;
};

struct xnn_ukernel_vunary {
  xnn_vunary_ukernel_fn function;
};

struct xnn_ukernel {
  enum xnn_microkernel_type type;
  // Used by subconv2d whether it is a GEMM or IGEMM.
  enum xnn_microkernel_type subtype;
  union {
    struct xnn_ukernel_conv2d conv2d;
    struct xnn_ukernel_dwconv dwconv;
    struct xnn_ukernel_dwconv2d dwconv2d;
    struct {
      struct xnn_ukernel_gemm gemm;
      struct xnn_ukernel_gemm gemm_nr2;
    };
    struct xnn_ukernel_igemm igemm;
    struct xnn_ukernel_spmm spmm;
    struct xnn_ukernel_vmulcaddc vmulcaddc;
    struct xnn_ukernel_vbinary vbinary;
    struct xnn_ukernel_vunary vunary;
  };
};

// Valid state transitions:
// - xnn_run_state_invalid -> xnn_run_state_skip
// - xnn_run_state_invalid -> xnn_run_state_ready
// - xnn_run_state_invalid -> xnn_run_state_needs_setup -> xnn_run_state_ready
enum xnn_run_state {
  // When an operator is first created, it starts off in invalid state, it needs to be setup, or reshape + setup.
  xnn_run_state_invalid = 0,
  // Operator is ready to be run.
  xnn_run_state_ready,
  // Operator doesn't need to be run.
  xnn_run_state_skip,
  // Operator has been reshaped, but not setup yet, pointers are not set.
  xnn_run_state_needs_setup,
};

struct xnn_operator {
  size_t batch_size;
  uint32_t padding_top;
  uint32_t padding_right;
  uint32_t padding_bottom;
  uint32_t padding_left;
  uint32_t kernel_height;
  uint32_t kernel_width;
  uint32_t stride_height;
  uint32_t stride_width;
  uint32_t dilation_height;
  uint32_t dilation_width;
  uint32_t groups;
  size_t group_channels;
  size_t group_input_channels;
  size_t group_output_channels;
  size_t channels;

  uint32_t pad_value;

  size_t input_height;
  size_t input_width;
  size_t input_pixel_stride;
  const void* input;
  const void** indirection_buffer;

  size_t output_height;
  size_t output_width;
  size_t output_pixel_stride;
  void* output;
  const void* quantization_params;

  size_t k_block_size;

  union {
    // Pointer to allocated packed weights. Use this if weights_cache is NULL.
    void* pointer;
    // Offset into the weights cache where the packed weights are. Only valid if weights_cache is not NULL.
    size_t offset;
  } packed_weights;
  // Stride between each set of packed weights.
  size_t weights_stride;
  // Total number of non-zero kernel elements when weights use sparse representation.
  size_t num_nonzero_values;
  // Total number of non-zero kernel blocks when weights use sparse representation.
  size_t num_nonzero_blocks;
  // Total number of output channel blocks when weights use sparse representation.
  size_t num_output_channel_blocks;
  // Input channel corresponding to the first non-zero kernel element.
  size_t first_input_channel;

  float input_scale;
  float output_scale;
  int32_t input_zero_point;

  size_t valid_batch_size;
  size_t last_input_height;
  size_t last_input_width;
  size_t last_input_channels;
  const void* last_input;
  size_t last_output_height;
  size_t last_output_width;
  void* last_output;
  uint32_t last_mr;

  uint32_t block_size;

  void* zero_buffer;
  void** zero_buffers;
  size_t zero_size;
  void* lookup_table;
  void* pixelwise_buffer;
  struct subconvolution_params* subconvolution_buffer;
  uint32_t flags;

  union {
    struct {
      uint32_t log2_element_size;
    } binary_elementwise;
    struct {
      uint32_t log2_input_size;
      uint32_t log2_output_size;
    } unary_elementwise;
    struct {
      uint32_t log2_data_element_size;
      uint32_t log2_accumulator_element_size;
    } reduce;
  };

  union {
    union xnn_binary_uparams binary;
    union xnn_unary_uparams unary;
    struct xnn_f16_default_params f16_default;
    struct xnn_f32_default_params f32_default;
    union xnn_f16_minmax_params f16_minmax;
    struct xnn_f16_scaleminmax_params f16_scaleminmax;
    struct xnn_reduce_params reduce;
    // Pixelwise Average Pooling normally use f32_minmax_params, but also initialize
    // f32_scaleminmax_params in case it needs to switch to Global Average Pooling operation.
    struct {
      union xnn_f32_minmax_params f32_minmax;
      struct xnn_f32_scaleminmax_params f32_scaleminmax;
    };
    struct xnn_f32_scale_params f32_scale;
    union xnn_f16_minmax_params f16_chw;
    union xnn_f32_minmax_params f32_chw;
    struct xnn_f32_qb4w_minmax_params f32_qb4w_minmax;
    struct xnn_f32_qc4w_minmax_params f32_qc4w_minmax;
    union xnn_qs8_conv_minmax_params qs8_conv_minmax;
    union xnn_qs8_qc8w_conv_minmax_params qs8_qc8w_conv_minmax;
    union xnn_qu8_conv_minmax_params qu8_conv_minmax;
    struct xnn_qu8_avgpool_minmax_params qu8_avgpool;
    struct xnn_s8_minmax_params s8_minmax;
    struct xnn_s32_default_params s32_default;
    struct xnn_u8_minmax_params u8_minmax;
  } params;
  // Second set of params. Operators like Dynamic Fully Connected only decides on the specific config to use during
  // reshape, so it needs to keep two sets of params around. Configs can have different initialization functions.
  // We also use this to store parameters to binary operators. For most such operators, this is a copy of params,
  // but params need to be swapped for commutative ops with per-operand params.
  union {
    union xnn_binary_uparams binary;
    union xnn_unary_uparams unary;
    struct xnn_f16_default_params f16_default;
    union xnn_f32_minmax_params f32_minmax;
    struct xnn_f32_default_params f32_default;
    struct xnn_s8_minmax_params s8_minmax;
    struct xnn_u8_minmax_params u8_minmax;
  } params2;
  // Third set of params. Used by scaled dot attention operator.
  union {
    struct xnn_f16_default_params f16_rmax;
    struct xnn_f32_default_params f32_rmax;
  } params3;
  // Fourth set of params. Used by scaled dot attention operator.
  union {
    union xnn_unary_uparams unary;
  } params4;
  enum xnn_operator_type type;
  struct xnn_ukernel ukernel;

  union {
    const struct xnn_argmaxpool_config* argmaxpool_config;
    struct {
      const struct xnn_avgpool_config* avgpool_config;
      const struct xnn_pavgpool_config* pavgpool_config;
      const struct xnn_reduce_config* rdsum_config;
      const struct xnn_reduce_config* rsum_config;
      const struct xnn_unary_elementwise_config* cvt_config;
    };
    const struct xnn_ibilinear_chw_config* ibilinear_chw_config;
    const struct xnn_ibilinear_config* ibilinear_config;
    struct {
      const struct xnn_rmax_config* rmax_config;
      union {
        // For QU8.
        const struct xnn_lut32norm_config* lut32norm_config;
        // For F16 and F32.
        struct {
          const struct xnn_raddstoreexpminusmax_config* raddstoreexpminusmax_config;
          const struct xnn_binary_elementwise_config* vmul_config;
        };
      };
    };  // For softmax operator.
    const struct xnn_maxpool_config* maxpool_config;
    const struct xnn_unpool_config* unpool_config;
    const struct xnn_zip_config* zip_config;
    struct {
      const struct xnn_xx_fill_config* fill_config;
      const struct xnn_xx_pad_config* pad_config;
    };  // For constant pad operator.
    const struct xnn_x8_lut_config* lut_config;
    const struct xnn_cmul_config* cmul_config;
    const struct xnn_transpose_config* transpose_config;
    const struct xnn_binary_elementwise_config* binary_elementwise_config;
    struct {
      const struct xnn_unary_elementwise_config* unary_elementwise_config;
      const struct xnn_reduce_config*
          rminmax_config;  // For dynamic quantization convert operator.
      const struct xnn_gemm_config*
          gemm_config;  // For dynamic quantization convert operator.
    };  // For unary elementwise operators.
    struct {
      const struct xnn_rmax_config* rmax_config;
      const struct xnn_raddstoreexpminusmax_config* raddstoreexpminusmax_config;
      const struct xnn_binary_elementwise_config* vadd_config;
      const struct xnn_binary_elementwise_config* vmul_config;
      const struct xnn_unary_elementwise_config* vtanh_config;
      enum xnn_attention_logits_cap_type cap_type;
      struct xnn_attention_logits_cap_tanh_params cap_params;
    } attention;  // For attention operator.
    const struct xnn_pack_lh_config* pack_lh_config;
  };

  struct compute_parameters compute[XNN_MAX_COMPUTE_INVOCATIONS];
  union {
    struct argmax_pooling_context argmax_pooling;
    struct average_pooling_context average_pooling;
    struct conv2d_context conv2d;
    struct dwconv2d_context dwconv2d;
    struct {
      struct dwconv_context dwconv;
      struct dwconv_indirection_init_context dwconv_indirection_init;
    } dwconv;
    struct elementwise_binary_context elementwise_binary;
    // PACKW GEMM GOI + GEMM are used together in Dynamic Fully Connected.
    struct {
      union {
        struct gemm_context gemm;
        struct scaled_dot_product_attention_context attention;
      } gemm;
      struct packw_gemm_goi_context packw_gemm_goi;
      struct packw_gemm_gio_context packw_gemm_gio;
      bool const_weights;
    } gemm;
    struct {
      struct igemm_context igemm;
      struct conv2d_igemm_indirection_init_context conv2d_igemm_indirection_init;
    } igemm;
    struct lut_contiguous_context lut_contiguous;
    struct lut_strided_context lut_strided;
    struct max_pooling_context max_pooling;
    struct pad_context pad;
    struct pixelwise_average_pooling_context pixelwise_average_pooling;
    struct reduce_context reduce;
    struct {
      struct resize_bilinear_context resize_bilinear;
      struct resize_bilinear_nhwc_indirection_init_context resize_nhwc_indirection_init;
    };
    struct resize_bilinear_chw_context resize_bilinear_chw;
    struct slice_context slice;
    struct spmm_context spmm;
    struct subconv_context subconv;
    struct subgemm_context subgemm;
    struct transpose_context transpose;
    struct floating_point_softmax_context floating_point_softmax;
    struct u8_softmax_context u8_softmax;
    struct f16_qd8_convert_context f16_qd8_convert;
    struct f32_qd8_convert_context f32_qd8_convert;
    struct f32_qp8_convert_context f32_qp8_convert;
    struct univector_contiguous_context univector_contiguous;
    struct univector_strided_context univector_strided;
    struct unpooling_context unpooling;
    struct vmulcaddc_context vmulcaddc;
    struct rope_context rope;
    struct x32_pack_lh_context x32_pack_lh;
  } context;

  struct xnn_code_cache* code_cache;
  xnn_weights_cache_t weights_cache;
  enum xnn_run_state state;
};

XNN_INTERNAL enum xnn_status xnn_run_operator_with_index(
  xnn_operator_t op,
  size_t opdata_index,
  size_t operator_object_index,
  pthreadpool_t threadpool);

XNN_INTERNAL enum xnn_operator_type xnn_reduce_operator_to_operator_type(enum xnn_reduce_operator op);

#ifdef __cplusplus
}  // extern "C"
#endif
