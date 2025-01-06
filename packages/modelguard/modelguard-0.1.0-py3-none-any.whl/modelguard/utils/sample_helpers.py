from numpy.typing import NDArray
import numpy as np


def add_batch_dimension(x: NDArray[np.float32]) -> NDArray[np.float32]:
    """Add a batch dimension to a single sample.

    Parameters
    ----------
    x
        The input sample to add a batch dimension to.

    Returns
    -------
    NDArray[np.float32]
        The input sample with a batch dimension added.

    """

    return np.expand_dims(x, axis=0)
