import logging

import numpy as np
from numpy.typing import NDArray

from modelguard.components import HookedModelOutput
from modelguard.model_monitors.model_monitor import ModelMonitor

logger = logging.getLogger(__name__)


class NullMonitor(ModelMonitor):
    """Null model monitoring technique.

    This class implements a null model monitoring technique that does nothing. This
    monitoring technique is useful for testing and as a placeholder when a model
    monitoring technique is not required.

    Attributes
    ----------
    required_model_hooks
        A list of the names of the model hooks required by the model monitoring technique
        to function. This model monitoring technique does not require any model hooks.
    is_fitted
        A boolean indicating whether the model monitoring technique has been fitted.

    """

    required_model_hooks: list[str] = []

    def __init__(self):
        """Initialize a null monitor technique."""
        super().__init__()

        logger.info("Initialized instance of NullMonitor")

    def fit(self, fit_data: HookedModelOutput):
        """Fit the null model monitoring technique.

        This method does not require fitting, so it does nothing.

        Parameters
        ----------
        fit_data
            The data to fit the model monitoring technique on.

        """
        logger.info(
            "Fitting NullMonitor instance ... "
            "This monitoring method does not require fitting, skipping ..."
        )

        self.set_fitted()

    def predict(self, x: HookedModelOutput) -> NDArray[np.float32]:
        """Make model performance predictions using the null model monitoring technique.

        This method does nothing and returns an array of zeros.

        Parameters
        ----------
        x
            The input data to make predictions on.

        Returns
        -------
        NDArray[np.float32]
            An array of zeros with the first dimension corresponding to the number of
            samples in the input data.

        """
        logger.info("Running inference on NullMonitor for " f"{len(x)} samples ...")

        self.check_fitted()

        logger.info(f"Finished inference on NullMonitor for " f"{len(x)} samples")

        return np.zeros(len(x)).astype(np.float32)
