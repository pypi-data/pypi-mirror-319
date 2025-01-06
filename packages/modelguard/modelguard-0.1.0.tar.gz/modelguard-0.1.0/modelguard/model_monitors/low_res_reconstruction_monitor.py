import logging

import numpy as np
import torch
from numpy.typing import NDArray
from torch.nn import MSELoss
from torch.nn.modules.loss import _Loss  # type: ignore
from torch.optim import AdamW
from torch.utils.data import TensorDataset, random_split

from modelguard.components.hooked_model_output import HookedModelOutput
from modelguard.config import Config
from modelguard.model_monitors.model_monitor import ModelMonitor
from modelguard.model_monitors.utils.models import LowResReconstructionDecoderModel
from modelguard.model_monitors.utils.trainers import LowResReconstructionDecoderTrainer
from modelguard.utils import run_torch_model_inference, set_global_seed

logger = logging.getLogger(__name__)


class LowResReconstructionMonitor(ModelMonitor):
    """Model monitoring technique based on a low-resolution decoder reconstruction
    error.

    This class implements an OOD detection technique based on the reconstruction error
    of a trained low-resolution sample reconstruction decoder. In this technique, an
    external decoder model is trained to reconstruct a low resolution version of the
    original input passed to the monitored model based on that model's latent space
    vector, i.e., for this technique to function, a decoder model needs to be trained
    to learn a mapping from an input latent space vector to a low resolution version of
    the original input passed to the monitored model.

    A reconstruction error is then computed as the mean squared error between the low
    resolution version of the target input data and the decoder-reconstructed data. A
    higher reconstruction error indicates that the input data is more likely to be an
    unseen sample, which in turn indicates that the model is more likely to be making
    wrong predictions.

    Attributes
    ----------
    required_model_hooks
        A list of the names of the model hooks required by the model monitoring technique
        to function. This OOD detection technique requires the `input` and
        `latent_vector` hooks to be attached to the model.

    """

    required_model_hooks: list[str] = ["input", "latent_vector"]

    def __init__(
        self,
        loss_fn: _Loss = MSELoss(),
        max_epochs: int = 500,
        early_stopping_patience: int = 10,
        train_batch_size: int = 32,
    ):
        """Initialize a low resolution reconstuction monitor instance.

        Parameters
        ----------
        loss_fn, optional
            An optional loss function for guiding the decoder model training, by
            default MSE loss.
        max_epochs, optional
            An optional limit on the maximum number of epochs for which to train the
            decoder model, by default 500.
        early_stopping_patience, optional
            An optional early stopping patience parameter that sets the maximum number
            of non-improving epoch results allowed before calling an early training
            stop, by default 10.
        train_batch_size, optional
            An optinal sample batch size to use when training the decoder model, by
            default 32.

        """
        super().__init__()

        self.decoder_model = None
        self.optimizer = None

        self.loss_fn = loss_fn
        self.max_epochs = max_epochs
        self.early_stopping_patience = early_stopping_patience
        self.train_batch_size = train_batch_size

        logger.info(
            "Initialized instance of LowResReconstructionMonitor "
            f"(loss fn: {loss_fn}, max epochs: {max_epochs}, "
            f"early stopping patience: {early_stopping_patience}, "
            f"train batch size: {train_batch_size})"
        )

    def fit(self, fit_data: HookedModelOutput):
        """Fit the low resolution reconstuction monitor technique.

        Parameters
        ----------
        fit_data
            The data to fit the model monitoring technique on.

        """
        logger.info("Fitting LowResReconstructionMonitor instance ...")

        # Set the seed for reproducability
        set_global_seed(Config.SEED)

        self.decoder_model = LowResReconstructionDecoderModel(
            out_channels=self._calculate_decoder_out_channels(fit_data)
        )
        self.optimizer = AdamW(self.decoder_model.parameters(), lr=1e-3)

        # Create a TensorDataset from the hooks data
        latent_vector_hook_data = torch.Tensor(
            fit_data["latent_vector"]  # input for the decoder
        )
        input_hook_data = torch.Tensor(fit_data["input"])  # target for the decoder
        data = TensorDataset(latent_vector_hook_data, input_hook_data)

        # Split the data for training
        train_data, val_data = random_split(data, [0.8, 0.2])

        logger.debug(
            "Fitting low-res reconstruction decoder model for "
            "LowResReconstructionMonitor"
        )

        # Train the underlying decoder model
        LowResReconstructionDecoderTrainer(
            model=self.decoder_model,
            train_data=train_data,
            val_data=val_data,
            loss_fn=self.loss_fn,
            optimizer=self.optimizer,
            max_epochs=self.max_epochs,
            early_stopping_patience=self.early_stopping_patience,
            train_batch_size=self.train_batch_size,
        ).fit()

        self.set_fitted()

        logger.info("Fitted LowResReconstructionMonitor instance")

    def _calculate_decoder_out_channels(self, fit_data: HookedModelOutput):
        """Calculate the required number of output channels for a decoder trying to
        reconstruct the `input` hook values of the fit data.

        Parameters
        ----------
        fit_data
            The data to fit the model monitoring technique on. Which we want to
            reconstruct using the decoder.

        Returns
        -------
            The required number of decoder output channels
        """

        # Get a single sanple
        input_hook_data_sample = fit_data["input"][0]

        return len(input_hook_data_sample)

    def predict(self, x: HookedModelOutput) -> NDArray[np.float32]:
        """Make model performance predictions using the low resolution reconstuction
        monitor technique.

        Parameters
        ----------
        x
            The input data to make predictions on.

        Returns
        -------
        NDArray[np.float32]
            The reconstruction errors between the low resolution input data and the
            reconstructed data. A higher reconstruction error indicates that the input
            data is more likely to be an unseen sample for which the model will likely
            make a wrong prediction.

            The shape of the returned numpy array is (N,), where N is the number of
            samples in the input data.

        """
        logger.info(
            "Running inference on LowResReconstructionMonitor for "
            f"{len(x)} samples ..."
        )

        self.check_fitted()

        if not self.decoder_model:
            raise ValueError(
                "Trying to run predict on the LowResReconstructionMonitor, but no "
                "decoder model instance set up. This should not be possible"
            )

        # Convert the input data to Tensors
        latent_vector_hook_data = torch.Tensor(
            x["latent_vector"]  # input for the decoder
        )
        input_hook_data = torch.Tensor(x["input"])  # target for the decoder

        # Get the outputs of the decoder model on the latent vectors
        decoder_reconstruction_data = run_torch_model_inference(
            self.decoder_model, latent_vector_hook_data
        )

        # Calculate the squared reconstruction loss per matching output to target
        # tensor cell.
        # The resulting output dims should thus be the same and not be reduced yet
        reconstruction_error = MSELoss(reduction="none")(
            decoder_reconstruction_data,
            LowResReconstructionDecoderTrainer.generate_low_res_version(
                input_hook_data
            ),
        )

        # Get the mean of the squared reconstruction losses across all dimensions of
        # the input sample except the batch dimension (axis 0)
        axis = tuple(range(1, len(x["input"].shape)))
        mean_reconstruction_error = torch.mean(reconstruction_error, axis)

        logger.info(
            f"Finished inference on LowResReconstructionMonitor for "
            f"{len(x)} samples"
        )

        return mean_reconstruction_error.numpy().astype(np.float32)  # type: ignore
