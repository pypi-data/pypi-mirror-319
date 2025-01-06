import logging
import random
import sys

import numpy as np
import torch

from modelguard.enums import VerbosityLevel


def set_global_seed(seed: int):
    """Set the seed value for the libraries used by ModelGuard that contain random
    operations.

    Parameters
    ----------
    seed
        The seed value to apply to the used libraries.

    """

    # General Python
    random.seed(seed)

    # PyTorch
    torch.manual_seed(seed)  # type: ignore

    # Numpy
    np.random.seed(seed)


def set_torch_determenistic_operations(enable: bool):
    """Set PyTorch to use determenistic operations whenever possible.

    See https://pytorch.org/docs/stable/notes/randomness.html for more information.

    Parameters
    ----------
    enable
        Wheter to enable the PyTorch determenistic operations.

    """

    # Disable cuDNN benchmarking operations that can cause non-determenistic behavior
    torch.backends.cudnn.benchmark = False if enable else True

    # Let PyTorch to use deterministic algorithms instead of nondeterministic ones
    # where available
    torch.use_deterministic_algorithms(enable)


def set_verbosity_level(level: VerbosityLevel):
    """Set the verbosity level for the modelguard package

    Parameters
    ----------
    level
        The verbosity level to set.

    """

    logger = logging.getLogger("modelguard")
    logger.setLevel(logging.DEBUG)

    # Remove any previous handlers for this module
    for handler in logger.handlers:
        logger.removeHandler(handler)

    verbosity_level_to_handler_level_conversion = {
        VerbosityLevel.OFF: logging.CRITICAL,
        VerbosityLevel.WARNING: logging.WARNING,
        VerbosityLevel.INFO: logging.INFO,
        VerbosityLevel.DEBUG: logging.DEBUG,
    }

    verbosity_handler = logging.StreamHandler(sys.stdout)
    verbosity_handler.setLevel(verbosity_level_to_handler_level_conversion[level])

    verbosity_handler_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    verbosity_handler.setFormatter(verbosity_handler_formatter)

    logger.addHandler(verbosity_handler)
