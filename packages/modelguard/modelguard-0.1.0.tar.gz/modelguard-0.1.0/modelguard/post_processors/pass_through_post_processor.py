from modelguard.post_processors.post_processor import PostProcessor
from numpy.typing import NDArray
import numpy as np


class PassThroughPostProcessor(PostProcessor):
    """Model monitor post-processing techniaue that passes the raw model monitor scores
    through without any post-processing.

    This post-processor is used when no post-processing is required on the raw model
    monitor scores. It simply returns the raw model monitor scores as is without any
    post-processing.

    """

    def fit(self, fit_data: NDArray[np.float32]):
        """Fit the pass-through post-processor.

        This post-processor does not require any fitting, so this method does nothing.

        Parameters
        ----------
        fit_data
            The data to fit the pass-through post-processor.

        """
        pass

        self.set_fitted()

    def predict(self, x: NDArray[np.float32]) -> NDArray[np.float32]:
        """Apply the pass-through post-processor to the input data.

        Since this is a pass-through post-processor, it simply returns the input data as
        is without any post-processing.

        Parameters
        ----------
        x
            The input data to apply the pass-through post-processor on.

        Returns
        -------
        NDArray[np.float64]
            The output of the pass-through post-processor, i.e. the input data as is
            without any post-processing.

        """
        self.check_fitted()

        return x
