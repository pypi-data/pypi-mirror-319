import logging

import numpy as np
from numpy.typing import NDArray

from modelguard.components.hooked_model_output import HookedModelOutput
from modelguard.model_monitors.model_monitor import ModelMonitor

logger = logging.getLogger(__name__)


class ContainedDecoderReconstructionMonitor(ModelMonitor):
    """Model monitoring technique based on the contained decoder reconstruction error.

    This class implements an OOD detection technique based on the reconstruction error
    of a model-contained decoder. The reconstruction error is computed as the mean
    squared error between the input data and the reconstructed data. A higher
    reconstruction error indicates that the input data is more likely to be an unseen
    sample, which in turn indicates that the model is more likely to be making wrong
    predictions.

    Note: This monitoring technique requires the model to already have a decoder in it
    for which we have access to the decoder output. This is a common setup in
    autoencoder models, where the decoder is used to reconstruct the input data. If a
    reconstruction decoder is not present in the model, this monitoring technique cannot
    be used.

    Attributes
    ----------
    required_model_hooks
        A list of the names of the model hooks required by the model monitoring technique
        to function. This OOD detection technique requires the `input` and
        `contained_decoder_output` hooks to be attached to the model.

    """

    required_model_hooks: list[str] = ["input", "contained_decoder_output"]

    def __init__(self):
        """Initialize a contained-decoder reconstruction monitor instance."""

        super().__init__()

        logger.info("Initialized instance of ContainedDecoderReconstructionMonitor")

    def fit(self, fit_data: HookedModelOutput):
        """Fit the contained decoder reconstruction model monitoring technique.

        This method does not require fitting, so it does nothing.

        Parameters
        ----------
        fit_data
            The data to fit the model monitoring technique on. This method does not
            require fitting, so this parameter is ignored.

        """
        logger.info(
            "Fitting ContainedDecoderReconstructionMonitor instance... "
            "This monitoring method does not require fitting, skipping ..."
        )

        self.set_fitted()

    def predict(self, x: HookedModelOutput) -> NDArray[np.float32]:
        """Make model performance predictions using the contained decoder reconstruction
        model monitoring technique.

        This method computes the reconstruction error between the model input data and
        the decoder-reconstructed data. The reconstruction error is computed as the
        mean squared error between the input data and the reconstructed data. A higher
        reconstruction error indicates a higher likelihood of wrong predictions by the
        model.

        Parameters
        ----------
        x
            The input data to make predictions on.

        Returns
        -------
        NDArray[np.float32]
            The reconstruction errors between the input data and the reconstructed data.
            A higher reconstruction error indicates that the input data is more likely
            to be an unseen sample for which the model will likely make a wrong
            prediction.

            The shape of the returned numpy array is (N,), where N is the number of
            samples in the input data.
        """
        logger.info(
            "Running inference on ContainedDecoderReconstructionMonitor for "
            f"{len(x)} samples ..."
        )

        self.check_fitted()

        # The axis containing the data along which we want to compute the mean squared
        # error should include all dimensions of the input sample except the batch
        # dimension (axis 0)
        axis = tuple(range(1, len(x["input"].shape)))

        # Compute the reconstruction error
        reconstruction_error = np.mean(
            (x["input"] - x["contained_decoder_output"]) ** 2,
            axis=axis,
            dtype=np.float32,
        )

        logger.info(
            f"Finished inference on ContainedDecoderReconstructionMonitor for "
            f"{len(x)} samples"
        )

        return reconstruction_error
