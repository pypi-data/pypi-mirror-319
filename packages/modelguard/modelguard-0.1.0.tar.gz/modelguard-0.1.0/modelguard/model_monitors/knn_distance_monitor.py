import logging
from typing import cast

import numpy as np
from numpy.typing import NDArray
from sklearn.neighbors import NearestNeighbors

from modelguard.components.hooked_model_output import HookedModelOutput
from modelguard.model_monitors.model_monitor import ModelMonitor

logger = logging.getLogger(__name__)


class KNNDistanceMonitor(ModelMonitor):
    """Model monitoring technique based on the k-nearest neighbors distance.

    This class implements a model monitoring technique based on the k-nearest neighbors
    distance of a sample's latent vector in comparison to the model's training samples'
    latent vectors. A higher distance indicates that the input data is more likely to be
    an unseen sample, which in turn indicates that the model is more likely to be making
    wrong predictions.

    This method is based on the paper "Out-of-Distribution Detection with Deep Nearest
    Neighbors" by Yiyou Sun et al. (2022).
    See `ref: https://proceedings.mlr.press/v162/sun22d.html`

    Attributes
    ----------
    required_model_hooks
        A list of the names of the model hooks required by the model monitoring technique
        to function. This OOD detection technique requires the `latent_vector` hook to be
        attached to the model.
    knn
        The underlying sklearn KNN model used for the distance computation.


    """

    required_model_hooks: list[str] = ["latent_vector"]

    def __init__(self, k: int = 50, distance_metric: str = "euclidean"):
        """Initialize a KNN distance model monitor instance.

        Parameters
        ----------
        k
            The number of nearest neighbors to consider for the distance computation.
        distance_metric
            The distance metric used for the distance computation.

        """

        super().__init__()

        self.knn = NearestNeighbors(n_neighbors=k, metric=distance_metric)

        logger.info(
            f"Initialized instance of KNNDistanceMonitor (k: {k}, distance metric: "
            f"{distance_metric})"
        )

    def fit(self, fit_data: HookedModelOutput):
        """Fit the KNN distance model monitor.

        This method fits the KNN model on the fit data's latent vectors.

        Parameters
        ----------
        fit_data
            The data to fit the model monitoring technique on.
        """
        logger.info("Fitting KNNDistanceMonitor instance ...")
        logger.debug(
            "Trainer of underlying KNN model does not export per-epoch training "
            "information"
        )

        self.knn.fit(fit_data["latent_vector"])  # type: ignore

        self.set_fitted()

        logger.info("Fitted KNNDistanceMonitor instance")

    def predict(self, x: HookedModelOutput) -> NDArray[np.float32]:
        """Make model performance predictions using the KNN distance model monitor.

        This method computes the mean distance between the input data's latent vectors
        and the k-nearest neighbors' latent vectors in the training data. A higher mean
        distance indicates a higher likelihood of wrong predictions by the model.

        Parameters
        ----------
        x
            The input data to make predictions on.

        Returns
        -------
        NDArray[np.float32]
            The mean KNN distances between the input data and the training data.
            A higher distance indicates that the input data is more likely to be OOD.

            The shape of the returned numpy array is (N,), where N is the number of
            samples in the input data.
        """
        logger.info(f"Running inference on KNNDistanceMonitor for {len(x)} samples ...")

        self.check_fitted()

        distances, _ = cast(
            tuple[NDArray[np.float64], NDArray[np.int64]],
            self.knn.kneighbors(x["latent_vector"]),  # type: ignore
        )
        mean_distances = distances.mean(axis=1, dtype=np.float32)

        logger.info(f"Finished inference on KNNDistanceMonitor for {len(x)} samples")

        return mean_distances
