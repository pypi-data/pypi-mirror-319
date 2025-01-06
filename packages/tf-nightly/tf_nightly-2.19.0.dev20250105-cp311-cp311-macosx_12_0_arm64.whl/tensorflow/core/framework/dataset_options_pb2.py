# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/framework/dataset_options.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorflow.core.framework import model_pb2 as tensorflow_dot_core_dot_framework_dot_model__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n/tensorflow/core/framework/dataset_options.proto\x12\x0ftensorflow.data\x1a%tensorflow/core/framework/model.proto\"\xb8\x02\n\x0f\x41utotuneOptions\x12\x11\n\x07\x65nabled\x18\x01 \x01(\x08H\x00\x12\x14\n\ncpu_budget\x18\x02 \x01(\x05H\x01\x12\x14\n\nram_budget\x18\x03 \x01(\x03H\x02\x12\x46\n\x12\x61utotune_algorithm\x18\x04 \x01(\x0e\x32(.tensorflow.data.model.AutotuneAlgorithmH\x03\x12\x1d\n\x13initial_parallelism\x18\x05 \x01(\x03H\x04\x42\x12\n\x10optional_enabledB\x15\n\x13optional_cpu_budgetB\x15\n\x13optional_ram_budgetB\x1d\n\x1boptional_autotune_algorithmB\x1e\n\x1coptional_initial_parallelism\"\xd1\x01\n\x12\x43\x61rdinalityOptions\x12G\n\rcompute_level\x18\x01 \x01(\x0e\x32\x30.tensorflow.data.CardinalityOptions.ComputeLevel\"r\n\x0c\x43omputeLevel\x12#\n\x1f\x43\x41RDINALITY_COMPUTE_UNSPECIFIED\x10\x00\x12\x1b\n\x17\x43\x41RDINALITY_COMPUTE_LOW\x10\x01\x12 \n\x1c\x43\x41RDINALITY_COMPUTE_MODERATE\x10\x02\"\x7f\n\x11\x44istributeOptions\x12;\n\x11\x61uto_shard_policy\x18\x01 \x01(\x0e\x32 .tensorflow.data.AutoShardPolicy\x12\x15\n\x0bnum_devices\x18\x02 \x01(\x05H\x00\x42\x16\n\x14optional_num_devices\"\xb9\x06\n\x13OptimizationOptions\x12%\n\x1b\x61pply_default_optimizations\x18\x01 \x01(\x08H\x00\x12\x17\n\rfilter_fusion\x18\x06 \x01(\x08H\x01\x12\x1e\n\x14map_and_batch_fusion\x18\t \x01(\x08H\x02\x12\x1f\n\x15map_and_filter_fusion\x18\n \x01(\x08H\x03\x12\x14\n\nmap_fusion\x18\x0b \x01(\x08H\x04\x12\x1d\n\x13map_parallelization\x18\x0c \x01(\x08H\x05\x12\x1a\n\x10noop_elimination\x18\x0e \x01(\x08H\x06\x12\x18\n\x0eparallel_batch\x18\x0f \x01(\x08H\x07\x12#\n\x19shuffle_and_repeat_fusion\x18\x11 \x01(\x08H\x08\x12 \n\x16\x66ilter_parallelization\x18\x12 \x01(\x08H\t\x12\x19\n\x0finject_prefetch\x18\x13 \x01(\x08H\n\x12!\n\x17seq_interleave_prefetch\x18\x15 \x01(\x08H\x0b\x42&\n$optional_apply_default_optimizationsB\x18\n\x16optional_filter_fusionB\x1f\n\x1doptional_map_and_batch_fusionB \n\x1eoptional_map_and_filter_fusionB\x15\n\x13optional_map_fusionB\x1e\n\x1coptional_map_parallelizationB\x1b\n\x19optional_noop_eliminationB\x19\n\x17optional_parallel_batchB$\n\"optional_shuffle_and_repeat_fusionB!\n\x1foptional_filter_parallelizationB\x1a\n\x18optional_inject_prefetchB\"\n optional_seq_interleave_prefetchJ\x04\x08\x02\x10\x03J\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06J\x04\x08\x07\x10\x08J\x04\x08\x08\x10\tJ\x04\x08\r\x10\x0eJ\x04\x08\x10\x10\x11J\x04\x08\x14\x10\x15\"5\n\x0eServiceOptions\x12\x10\n\x06pinned\x18\x01 \x01(\x08H\x00\x42\x11\n\x0foptional_pinned\"\xa2\x01\n\x10ThreadingOptions\x12\"\n\x18max_intra_op_parallelism\x18\x01 \x01(\x05H\x00\x12!\n\x17private_threadpool_size\x18\x02 \x01(\x05H\x01\x42#\n!optional_max_intra_op_parallelismB\"\n optional_private_threadpool_size\"\xb5\x05\n\x07Options\x12\x16\n\x0c\x64\x61taset_name\x18\n \x01(\tH\x00\x12\x16\n\x0e\x66ramework_type\x18\x0b \x03(\t\x12\x17\n\rdeterministic\x18\x01 \x01(\x08H\x01\x12:\n\x10\x61utotune_options\x18\x07 \x01(\x0b\x32 .tensorflow.data.AutotuneOptions\x12>\n\x12\x64istribute_options\x18\x02 \x01(\x0b\x32\".tensorflow.data.DistributeOptions\x12\x42\n\x14optimization_options\x18\x03 \x01(\x0b\x32$.tensorflow.data.OptimizationOptions\x12\x38\n\x0fservice_options\x18\x0c \x01(\x0b\x32\x1f.tensorflow.data.ServiceOptions\x12\x0f\n\x05slack\x18\x04 \x01(\x08H\x02\x12<\n\x11threading_options\x18\x05 \x01(\x0b\x32!.tensorflow.data.ThreadingOptions\x12\x45\n\x15\x65xternal_state_policy\x18\x06 \x01(\x0e\x32$.tensorflow.data.ExternalStatePolicyH\x03\x12\x1d\n\x13symbolic_checkpoint\x18\x08 \x01(\x08H\x04\x12\x14\n\nwarm_start\x18\t \x01(\x08H\x05\x42\x17\n\x15optional_dataset_nameB\x18\n\x16optional_deterministicB\x10\n\x0eoptional_slackB \n\x1eoptional_external_state_policyB\x1e\n\x1coptional_symbolic_checkpointB\x15\n\x13optional_warm_start*K\n\x0f\x41utoShardPolicy\x12\x08\n\x04\x41UTO\x10\x00\x12\x08\n\x04\x46ILE\x10\x01\x12\x08\n\x04\x44\x41TA\x10\x02\x12\x08\n\x04HINT\x10\x03\x12\x10\n\x03OFF\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01*J\n\x13\x45xternalStatePolicy\x12\x0f\n\x0bPOLICY_WARN\x10\x00\x12\x11\n\rPOLICY_IGNORE\x10\x01\x12\x0f\n\x0bPOLICY_FAIL\x10\x02\x42XZVgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/dataset_options_go_protob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.core.framework.dataset_options_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZVgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/dataset_options_go_proto'
  _AUTOSHARDPOLICY._serialized_start=2507
  _AUTOSHARDPOLICY._serialized_end=2582
  _EXTERNALSTATEPOLICY._serialized_start=2584
  _EXTERNALSTATEPOLICY._serialized_end=2658
  _AUTOTUNEOPTIONS._serialized_start=108
  _AUTOTUNEOPTIONS._serialized_end=420
  _CARDINALITYOPTIONS._serialized_start=423
  _CARDINALITYOPTIONS._serialized_end=632
  _CARDINALITYOPTIONS_COMPUTELEVEL._serialized_start=518
  _CARDINALITYOPTIONS_COMPUTELEVEL._serialized_end=632
  _DISTRIBUTEOPTIONS._serialized_start=634
  _DISTRIBUTEOPTIONS._serialized_end=761
  _OPTIMIZATIONOPTIONS._serialized_start=764
  _OPTIMIZATIONOPTIONS._serialized_end=1589
  _SERVICEOPTIONS._serialized_start=1591
  _SERVICEOPTIONS._serialized_end=1644
  _THREADINGOPTIONS._serialized_start=1647
  _THREADINGOPTIONS._serialized_end=1809
  _OPTIONS._serialized_start=1812
  _OPTIONS._serialized_end=2505
# @@protoc_insertion_point(module_scope)
