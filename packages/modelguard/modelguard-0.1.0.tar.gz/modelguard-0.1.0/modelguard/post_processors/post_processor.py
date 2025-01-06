from numpy.typing import NDArray
import numpy as np


class PostProcessor:
    """The base class for model monitor post-processing techniques.

    This class defines the interface for a model monitor post-processing technique. All
    model monitor post-processing techniques should inherit from this class and implement
    the `fit` and `predict` methods.

    The `fit` method is used to optionally fit the model monitor post-processing
    technique to the specific outputs of the model monitor for which we want to use
    the post-processing technique. Some model monitor post-processing techniques require
    this fitting on the model monitor outputs, while others do not.

    The `predict` method is used to make predictions on the input data. The method should
    return a float value representing the post-processed model monitor score for each
    input raw model monitor score. The resulting post-processed monitoring scores are
    stored in a numpy array, where each element corresponds to the post-processed
    monitoring score for the corresponding input raw model monitor score.

    """

    def __init__(self):
        """Initialize the model monitor post-processing technique."""
        self.is_fitted = False

    def fit(self, fit_data: NDArray[np.float32]) -> None:
        """Fit the model monitor post-processing technique.

        Parameters
        ----------
        fit_data
            The data to fit the model monitor post-processing technique.
        """
        raise NotImplementedError

    def predict(self, x: NDArray[np.float32]) -> NDArray[np.float32]:
        """Make model monitor post-processing predictions using the model monitor
        post-processing technique.

        Parameters
        ----------
        x
            The input data to make predictions on.
        """
        raise NotImplementedError

    def check_fitted(self):
        """Check if the model monitor post-processing technique is fitted.

        Raises
        ------
        ValueError
            If the model monitor post-processing technique is not fitted.
        """

        if not self.is_fitted:
            raise ValueError(
                "The model monitor post-processing technique is not fitted. Please run the `fit` method first."
            )

    def set_fitted(self):
        """Set the model monitor post-processing technique as fitted."""
        self.is_fitted = True
