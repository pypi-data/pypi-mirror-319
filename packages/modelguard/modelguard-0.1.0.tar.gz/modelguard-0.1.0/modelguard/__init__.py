# type: ignore
import logging

from modelguard.benchmark import Benchmark
from modelguard.enums import VerbosityLevel
from modelguard.hooked_onnx_model import HookedONNXModel
from modelguard.monitored_model import MonitoredModel
from modelguard.utils import set_torch_determenistic_operations, set_verbosity_level

logger = logging.getLogger("modelguard")

set_torch_determenistic_operations(False)
set_verbosity_level(VerbosityLevel.WARNING)

__all__ = ["Benchmark", "HookedONNXModel", "MonitoredModel"]
