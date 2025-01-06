from numpy.typing import NDArray
import numpy as np


class MonitoredModelOutput:
    """Container class to store the outputs a monitored model inference step.

    Attributes
    ----------
    model_outputs
        The outputs of the contained model of the monitored model instance. The shape
        of the numpy array is (N, ...), where N is the number of samples that were
        passed through the model during inference and the remaining dimensions depend on
        the model's specific output shape.
    model_monitor_outputs
        The outputs of the model monitor. The shape of the numpy array is (N,), where N
        is the number of samples that were passed through the model during inference.
    post_processor_outputs
        The outputs of the post-processor applied to the model monitor outputs. The shape
        of the numpy array is (N,), where N is the number of samples that were passed
        through the model during inference.

    """

    def __init__(
        self,
        model_outputs: NDArray[np.float32],
        model_monitor_outputs: NDArray[np.float32],
        post_processor_outputs: NDArray[np.float32],
    ):
        """Initialize a MonitoredModelOutput instance.

        Parameters
        ----------
        model_outputs
            The outputs of the contained model of the monitored model instance. The shape
            of the numpy array is (N, ...), where N is the number of samples that were
            passed through the model during inference and the remaining dimensions depend on
            the model's specific output shape.
        model_monitor_outputs
            The outputs of the model monitor. The shape of the numpy array is (N,), where N
            is the number of samples that were passed through the model during inference.
        post_processor_outputs
            The outputs of the post-processor applied to the model monitor outputs. The shape
            of the numpy array is (N,), where N is the number of samples that were passed
            through the model during inference.

        """
        self.model_outputs = model_outputs
        self.model_monitor_outputs = model_monitor_outputs
        self.post_processor_outputs = post_processor_outputs

    def __getitem__(
        self, idx: int
    ) -> tuple[NDArray[np.float32], NDArray[np.float32], NDArray[np.float32]]:
        """Get the outputs of the monitored model instance at the given sample index.

        Parameters
        ----------
        idx
            The index of the outputs to retrieve.

        Returns
        -------
        tuple[NDArray[np.float32], NDArray[np.float32], NDArray[np.float32]]
            A tuple containing the model outputs, the model monitor outputs and the
            post-processor outputs, respectively, at the given index.

        """

        return (
            self.model_outputs[idx],
            self.model_monitor_outputs[idx],
            self.post_processor_outputs[idx],
        )
