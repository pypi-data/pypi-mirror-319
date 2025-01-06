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


class EnsembleLowResReconstructionMonitor(ModelMonitor):
    """Model monitoring technique based on the reconstruction differences of an ensemble
    of different low-resolution decoders.

    This class implements an OOD detection technique based on the reconstruction
    differences of an ensemble of trained low-resolution sample reconstruction
    decoders. In this technique, an ensemble of external decoder models is trained to
    reconstruct a low resolution version of the original input passed to the monitored
    model based on that model's latent space vector, i.e., for this technique to
    function, each decoder model needs to be trained to learn a mapping from an input
    latent space vector to a low resolution version of the original input passed to
    the monitored model.

    The variance between the different decoder models in the ensemble is then
    computed. A higher variance indicates that the input data is more likely to be an
    unseen sample, which in turn indicates that the model is more likely to be making
    wrong predictions.

    Attributes
    ----------
    required_model_hooks
        A list of the names of the model hooks required by the model monitoring
        technique to function. This OOD detection technique requires the `input` and
        `latent_vector` hooks to be attached to the model.

    """

    required_model_hooks: list[str] = ["input", "latent_vector"]

    def __init__(
        self,
        num_decoders: int,
        loss_fn: _Loss = MSELoss(),
        max_epochs: int = 500,
        early_stopping_patience: int = 10,
        train_batch_size: int = 32,
    ):
        """Initialize an ensemble low resolution reconstruction monitor instance.

        Parameters
        ----------
        num_decoders
            The number of low resolution reconstruction decoder models to include
            in the ensemble.
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

        self.ensemble_models: list[LowResReconstructionDecoderModel] = []

        self.num_decoders = num_decoders
        self.loss_fn = loss_fn
        self.max_epochs = max_epochs
        self.early_stopping_patience = early_stopping_patience
        self.train_batch_size = train_batch_size

        logger.info(
            "Initialized instance of EnsembleLowResReconstructionMonitor "
            f"(num of decoders: {num_decoders}, loss fn: {loss_fn}, "
            f"max epochs: {max_epochs}, "
            f"early stopping patience: {early_stopping_patience}, "
            f"train batch size: {train_batch_size})"
        )

    def fit(self, fit_data: HookedModelOutput):
        """Fit the monitor technique.

        Parameters
        ----------
        fit_data
            The data to fit the model monitoring technique on.

        """
        logger.info("Fitting EnsembleLowResReconstructionMonitor instance ...")

        # Set the seed for reproducability
        set_global_seed(Config.SEED)

        # Initialize the ensemble of different decoder models
        for _ in range(self.num_decoders):
            self.ensemble_models.append(
                LowResReconstructionDecoderModel(
                    out_channels=self._calculate_decoder_out_channels(fit_data)
                )
            )

        # Create a TensorDataset from the hooks data
        latent_vector_hook_data = torch.Tensor(
            fit_data["latent_vector"]  # input for the decoder
        )
        input_hook_data = torch.Tensor(fit_data["input"])  # target for the decoder
        data = TensorDataset(latent_vector_hook_data, input_hook_data)

        # Split the data for training
        train_data, val_data = random_split(data, [0.8, 0.2])

        # Train the each decoder model in the ensemble seperately
        for i, decoder_model in enumerate(self.ensemble_models):
            logger.debug(
                f"Fitting nr. {i+1} (of {self.num_decoders}) low-res reconstruction "
                "decoder models for EnsembleLowResReconstructionMonitor"
            )

            LowResReconstructionDecoderTrainer(
                model=decoder_model,
                train_data=train_data,
                val_data=val_data,
                loss_fn=self.loss_fn,
                optimizer=AdamW(decoder_model.parameters(), lr=1e-3),
                max_epochs=self.max_epochs,
                early_stopping_patience=self.early_stopping_patience,
                train_batch_size=self.train_batch_size,
            ).fit()

        logger.info("Fitted EnsembleLowResReconstructionMonitor instance")

        self.set_fitted()

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
        """Make model performance predictions using monitor technique.

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
            "Running inference on EnsembleLowResReconstructionMonitor for "
            f"{len(x)} samples ..."
        )

        self.check_fitted()

        # Convert the needed input data to Tensors
        latent_vector_hook_data = torch.Tensor(
            x["latent_vector"]  # input for the decoder
        )

        # Get the outputs of the each decoder model in the ensemble on the latent
        # vectors and stack them so that this new ensemble stacked tensor has a shape
        # of (N, E, *R), with N the batch dim, E the stacked ensemble dim and *R the
        # tuple of the decoder reconstruction output shape.
        decoder_reconstructions_data = torch.stack(
            [
                run_torch_model_inference(decoder_model, latent_vector_hook_data)
                for decoder_model in self.ensemble_models
            ],
            dim=1,
        )

        # Calculate the variance for each element in the decoder reconstruction tensor
        # across the ensemble of different decoders (this also keeps the batch dim).
        # Out shape: (N, *R)
        decoder_reconstructions_variance = torch.var(
            decoder_reconstructions_data, dim=1
        )

        # Calculate the mean ensemble decoder reconstruction variance per sample in the
        # input batch in order to get a per-sample monitor score.
        # Out shape: (N)
        axis = tuple(range(1, len(decoder_reconstructions_variance.shape)))
        mean_decoder_reconstructions_variance = torch.mean(
            decoder_reconstructions_variance, dim=axis
        )

        logger.info(
            f"Finished inference on EnsembleLowResReconstructionMonitor for "
            f"{len(x)} samples"
        )

        return mean_decoder_reconstructions_variance.numpy().astype(np.float32)  # type: ignore
