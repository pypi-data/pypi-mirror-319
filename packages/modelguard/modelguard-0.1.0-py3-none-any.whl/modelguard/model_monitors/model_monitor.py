import numpy as np
from numpy.typing import NDArray

from modelguard.components.hooked_model_output import HookedModelOutput


class ModelMonitor:
    """The base class for model monitoring techniques.

    This class defines the interface for a model monitoring technique. All model
    monitoring techniques should inherit from this class and implement the `fit` and
    `predict` methods.

    The `fit` method is used to optionally fit the model monitoring technique on some
    fitting data. Some model monitoring techniques require this step, while others do
    not. For example, distance-based model monitoring requires fitting in order to
    compute the distance threshold based on the fitting data. Note that the child
    class should still call the parent class's `fit` method to ensure that the
    `is_fitted` attribute is set to `True`.

    The `predict` method is used to make predictions on the input data. The method
    should return a float value representing the model monitoring score for the each
    input sample. The resulting monitoring scores are stored in a numpy array, where
    each element corresponds to the monitoring score for the corresponding input sample.

    Attributes
    ----------
    required_model_hooks
        A list of the names of the model hooks required by the model monitoring
        technique to function.
        TODO: Add more details about what a model hook is and how it is used (e.g. link
        to the documentation for the MonitoredModel class).

    """

    required_model_hooks: list[str] = []

    def __init__(self):
        """Initialize a model monitoring technique."""
        self.is_fitted = False

    def fit(self, fit_data: HookedModelOutput) -> None:
        """Fit the model monitoring technique.

        Parameters
        ----------
        fit_data
            The data to fit the model monitoring technique.
        """
        raise NotImplementedError

    def predict(self, x: HookedModelOutput) -> NDArray[np.float32]:
        """Make model performance predictions using the model monitoring technique.

        Parameters
        ----------
        x
            The input data to make predictions on.

        Returns
        -------
        NDArray[np.float32]
            The model monitoring scores for the input data.

        """
        raise NotImplementedError

    def check_fitted(self):
        """Check if the model monitoring technique is fitted.

        Raises
        ------
        ValueError
            If the model monitoring technique is not fitted.
        """

        if not self.is_fitted:
            raise ValueError(
                "The model monitoring technique is not fitted. Please run the `fit` method first."
            )

    def set_fitted(self):
        """Set the model monitoring technique as fitted."""
        self.is_fitted = True
