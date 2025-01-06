from modelguard.post_processors.post_processor import PostProcessor
from numpy.typing import NDArray
import numpy as np


class MaxThresholdPostProcessor(PostProcessor):
    """Model monitor post-processing technique that applies a threshold to the model
    monitor's output based on the maximum monitor score for a collection of fit data
    samples.

    The threshold of this post-processor is set to the maximum monitor score given to a
    collection of fit data samples, multiplied by an optional `threshold_multiplier`.
    Formally, the threshold is calculated as:

    .. math::

        threshold = threshold_multiplier * max(monitor_scores)


    Parameters
    ----------
    left_value
        The value to return if the monitor score is less than or equal to the threshold.
    right_value
        The value to return if the monitor score is greater than the threshold.
    threshold_multiplier
        The multiplier to apply to the maximum monitor score to set the threshold. A
        multiplier of 1.0, means the original maximum monitor score is used as is to
        set the threshold.
    threshold
        The threshold value that is used for the post-processor. This threshold value
        is calculated and set in the `fit` method.

    """

    def __init__(
        self,
        left_value: float = 0.0,
        right_value: float = 1.0,
        threshold_multiplier: float = 1.0,
    ):
        """Initialize the threshold post-processor.

        Parameters
        ----------
        left_value, optional
            The value to return if the monitor score is less than or equal to the
            threshold. The default is 0.0.
        right_value, optional
            The value to return if the monitor score is greater than the threshold. The
            default is 1.0.
        threshold_multiplier, optional
            The multiplier to apply to the maximum monitor score to set the threshold.
            The default is 1.0, which means the original maximum monitor score is used
            as is to set the threshold.
        """
        super().__init__()

        self.left_value = left_value
        self.right_value = right_value
        self.threshold_multiplier = threshold_multiplier
        self.threshold = None

    def fit(self, fit_data: NDArray[np.float32]):
        """Fit the threshold post-processor.

        This method calculates the threshold value for the post-processor based on the
        maximum monitor score for the provided collection of fit data samples multiplied
        by the MaxThresholdPostProcessor's `threshold_multiplier` attribute.

        Parameters
        ----------
        fit_data
            The data to fit the threshold post-processor.
        """

        self.threshold = float(np.max(fit_data) * self.threshold_multiplier)

        self.set_fitted()

    def predict(self, x: NDArray[np.float32]) -> NDArray[np.float32]:
        """Apply the threshold post-processor to the monitor scores.

        Attributes
        ----------
        x
            The monitor scores to apply the max threshold post-processor on.

        Returns
        -------
        NDArray[np.float32]
            The thresholded monitor scores. If the monitor score is less than or equal
            to the threshold, the left value is returned. Otherwise, the right value is
            returned.

        """
        self.check_fitted()

        if self.threshold is None:
            raise ValueError(
                "The threshold post-processor has not been set yet, this should not happen. \
                the `check_fitted` method should have raised an error."
            )

        # Apply the threshold to the monitor scores
        return np.where(x <= self.threshold, self.left_value, self.right_value).astype(
            np.float32
        )
