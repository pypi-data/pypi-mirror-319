# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.train.experimental namespace
"""

import sys as _sys

from tensorflow.python.checkpoint.sharding.sharding_policies import MaxShardSizePolicy # line: 74
from tensorflow.python.checkpoint.sharding.sharding_policies import ShardByTaskPolicy # line: 37
from tensorflow.python.checkpoint.sharding.sharding_util import ShardableTensor # line: 40
from tensorflow.python.checkpoint.sharding.sharding_util import ShardingCallback # line: 76
from tensorflow.python.trackable.python_state import PythonState # line: 28
from tensorflow.python.training.experimental.loss_scale import DynamicLossScale # line: 300
from tensorflow.python.training.experimental.loss_scale import FixedLossScale # line: 203
from tensorflow.python.training.experimental.loss_scale import LossScale # line: 37
from tensorflow.python.training.experimental.loss_scale_optimizer import MixedPrecisionLossScaleOptimizer # line: 29
from tensorflow.python.training.experimental.mixed_precision import disable_mixed_precision_graph_rewrite_v1 as disable_mixed_precision_graph_rewrite # line: 218
from tensorflow.python.training.experimental.mixed_precision import enable_mixed_precision_graph_rewrite_v1 as enable_mixed_precision_graph_rewrite # line: 82

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "train.experimental", public_apis=None, deprecation=False,
      has_lite=False)
