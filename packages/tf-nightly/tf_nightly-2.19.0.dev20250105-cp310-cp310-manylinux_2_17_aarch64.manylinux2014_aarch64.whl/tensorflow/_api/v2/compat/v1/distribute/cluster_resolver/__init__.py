# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.distribute.cluster_resolver namespace
"""

import sys as _sys

from tensorflow.python.distribute.cluster_resolver.cluster_resolver import ClusterResolver # line: 55
from tensorflow.python.distribute.cluster_resolver.cluster_resolver import SimpleClusterResolver # line: 288
from tensorflow.python.distribute.cluster_resolver.cluster_resolver import UnionClusterResolver as UnionResolver # line: 418
from tensorflow.python.distribute.cluster_resolver.gce_cluster_resolver import GCEClusterResolver # line: 30
from tensorflow.python.distribute.cluster_resolver.kubernetes_cluster_resolver import KubernetesClusterResolver # line: 23
from tensorflow.python.distribute.cluster_resolver.slurm_cluster_resolver import SlurmClusterResolver # line: 163
from tensorflow.python.distribute.cluster_resolver.tfconfig_cluster_resolver import TFConfigClusterResolver # line: 47
from tensorflow.python.distribute.cluster_resolver.tpu_cluster_resolver import TPUClusterResolver # line: 24

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "distribute.cluster_resolver", public_apis=None, deprecation=False,
      has_lite=False)
