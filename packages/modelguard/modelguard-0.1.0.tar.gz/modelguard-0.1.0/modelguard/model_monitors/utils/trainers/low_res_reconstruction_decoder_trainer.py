import logging
from typing import TypeVar, cast

import numpy as np
import torch
from torch.nn import Module
from torch.nn.functional import interpolate  # type: ignore
from torch.nn.modules.loss import _Loss  # type: ignore
from torch.optim import Optimizer
from torch.utils.data import DataLoader, Dataset

from modelguard.config import Config

T = TypeVar("T")

logger = logging.getLogger(__name__)


class LowResReconstructionDecoderTrainer:
    """A trainer class for training a low-resolution reconstruction decoder model"""

    def __init__(
        self,
        model: Module,
        train_data: Dataset[T],
        val_data: Dataset[T],
        loss_fn: _Loss,
        optimizer: Optimizer,
        max_epochs: int,
        early_stopping_patience: int = 10,
        train_batch_size: int = 32,
    ):
        """Initialize the Low-resolution reconstrcution decoder model trainer instance

        Parameters
        ----------
        model
            The decoder model to train.
        train_data
            The training dataset.
        val_data
            The validation dataset.
        loss_fn
            The loss function.
        optimizer
            The training optimizer
        max_epochs
            The maximum number of epochs to train the model for.
        early_stopping_patience
            The amount of consecutive times for which we can accept a non-improving
            validation loss value (i.e. lower value) before calling an early training
            stop.
        train_batch_size, optional
            The sample batch size to use during training, by default 32.

        """

        self.model = model
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.max_epochs = max_epochs
        self.early_stopping_patience = early_stopping_patience
        self.train_dataloader = DataLoader(
            train_data,
            batch_size=train_batch_size,
            shuffle=True,
            num_workers=Config.DATALOADER_NUM_WORKERS,
        )
        self.val_dataloader = DataLoader(
            val_data,
            batch_size=1,
            shuffle=False,
            num_workers=0,
        )

        # Set the early stopping start attributes
        self.lowest_val_loss = float("inf")
        self.num_non_improving_epochs = 0

    def fit(self):
        """Fit the trainer setup"""

        self.model.to(Config.DEVICE)

        early_stop = False
        epoch = 0
        while not early_stop and epoch < self.max_epochs:
            self.model.train()
            mean_train_loss = self._train_one_epoch()

            self.model.eval()
            mean_val_loss = self._eval_one_epoch()

            # Check if the training should be stopped early for non-improving
            # performance
            early_stop = self._early_stopping(mean_val_loss)

            epoch += 1

            logger.debug(
                f"epoch: {epoch}, mean_train_loss: {mean_train_loss}, mean_val_loss: {mean_val_loss}"
            )
            if early_stop:
                logger.debug("EARLY STOPPING ...")

        self.model.cpu()

    def _train_one_epoch(self) -> float:
        """Train the contained model for one epoch.

        Returns
        -------
        float
            The mean training loss for this epoch.

        """

        losses_this_epoch: list[float] = []

        for _, data in enumerate(self.train_dataloader):

            # Extract the feature (x) and target (y) components of the data
            x, y = data

            # Generate low-res versions of the target that the model will try to
            # reconstruct
            y = LowResReconstructionDecoderTrainer.generate_low_res_version(y)

            x, y = x.to(Config.DEVICE), y.to(Config.DEVICE)

            # Zero the gradients for the new input data batch
            self.optimizer.zero_grad()

            # Run inference on the model
            model_out = self.model(x)

            # Calculate the loss and gradients
            loss = self.loss_fn(model_out, y)
            losses_this_epoch.append(loss.item())
            loss.backward()

            # Update model weights
            self.optimizer.step()

        return np.mean(losses_this_epoch).item()

    def _eval_one_epoch(self) -> float:
        """Evaluate the contained model for one epoch

        Returns
        -------
        float
            The mean evaluation loss for this epoch.

        """

        losses_this_epoch: list[float] = []

        with torch.no_grad():
            for _, data in enumerate(self.val_dataloader):

                # Extract the feature (x) and target (y) components of the data
                x, y = data

                # Generate low-res versions of the target that the model will try to
                # reconstruct
                y = LowResReconstructionDecoderTrainer.generate_low_res_version(y)

                x, y = x.to(Config.DEVICE), y.to(Config.DEVICE)

                # Run inference on the model
                model_out = self.model(x)

                # Calculate the loss and gradients
                loss = self.loss_fn(model_out, y)
                losses_this_epoch.append(loss.item())

        return np.mean(losses_this_epoch).item()

    @staticmethod
    def generate_low_res_version(x: torch.Tensor) -> torch.Tensor:
        """Generate low resoultion versions of a batch of samples of the same shape
        that the decoder model will need to reconstrcut.

        This method will reshape a batch of samples to a height and width dimension of
        (16 x 16) while keeping the original batch and channel dimensions. The final
        output dimension of the sample batch should thus be: (N, C, 16, 16) with `N` the
        batch dimension and `C` the channel dimension.

        Parameters
        ----------
        x
            The batch of samples for which to generate low resolution versions

        Returns
        -------
        Tensor
            The reshaped batch of samples with shape: (N, C, 16, 16)

        """

        # The `interploate` function ignores the batch and channel dimension
        # information
        x = interpolate(x, (16, 16), mode="bilinear")  # type: ignore

        x = cast(torch.Tensor, x)

        return x

    def _early_stopping(self, mean_val_loss: float) -> bool:
        """Determine if the training should be stopped early based on non-improving
        performance.

        The decision to stop is made when the consecutive number of epochs where the
        mean validation loss has not been improved (i.e. lowered) exceeds a set
        `early_stopping_patience` value.

        Parameters
        ----------
        mean_val_loss
            The mean validation loss of the latest epoch

        Returns
        -------
        bool
            Return True if the training should be stopped early, otherwise False.
        """

        if mean_val_loss < self.lowest_val_loss:
            # If an improved model has been found, reset the early stopping attributes
            self.num_non_improving_epochs = 0

            # Update the lowest val loss
            self.lowest_val_loss = mean_val_loss

            return False
        else:
            self.num_non_improving_epochs += 1

            if self.num_non_improving_epochs > self.early_stopping_patience:
                return True
            else:
                return False
