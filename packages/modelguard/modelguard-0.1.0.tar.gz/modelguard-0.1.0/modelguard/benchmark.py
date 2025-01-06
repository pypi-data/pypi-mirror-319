import numpy as np
from numpy.typing import NDArray

from modelguard.components import BenchmarkResult, MonitoredModelOutput
from modelguard.evaluators import Evaluator
from modelguard.monitored_model import MonitoredModel


class Benchmark:
    """Class to manage the benchmarking of a model with different model monitoring
    techniques.

    Attributes
    ----------
    monitored_models
        Dict containing the monitored model instances we want to benchmark. The keys are
        the names of the model monitoring techniques and the values are the
        corresponding MonitoredModel instances.

    """

    def __init__(self, monitored_models: dict[str, MonitoredModel]):
        """Initialize a Benchmark instance.

        Parameters
        ----------
        monitored_models
            Dict containing the monitored model instances we want to benchmark. The keys are
            the names of the model monitoring techniques and the values are the
            corresponding MonitoredModel instances.

        """

        self.monitored_models = monitored_models

    def run(
        self,
        fit_data: NDArray[np.float32],
        in_distribution_data: dict[str, NDArray[np.float32]],
        out_of_distribution_data: dict[str, NDArray[np.float32]],
    ):
        """Run the benchmarking pipeline on the given data.

        The benchmarking pipeline consists of the following steps:
        1. Fit the monitored model instances on the given fit data.
        2. Run the predict step of the fitted monitored models on the in-distribution and
           out-of-distribution data.
        3. Evaluate the monitored model outputs.

        Parameters
        ----------
        fit_data
            The data to use for fitting the model monitors.
        in_distribution_data
            Dict containing the in-distribution validation data to use for the benchmark.
            The keys are the names of the in-distribution datasets and the values are the
            corresponding data arrays.
        out_of_distribution_data
            Dict containing out-of-distribution data to use for the benchmark. The keys
            are the names of the out-of-distribution datasets and the values are the
            corresponding data arrays.

        """

        # Fit the monitored models
        self.fit(fit_data)

        # Run the predict step of the fitted monitored models
        benchmark_result = self.predict(in_distribution_data, out_of_distribution_data)

        # Evaluate the monitored model outputs.
        self.evaluate(benchmark_result)

    def fit(self, fit_data: NDArray[np.float32]):
        """Fit the monitored model instances' monitoring techniques on the contained
        model based on the given fit data.

        This fitting step first sends the fit data through the hooked model to get the
        hook outputs. Then, the model monitor is fitted on these hook outputs.

        Parameters
        ----------
        fit_data
            The data to use for fitting the model monitors.

        """

        # Send the fit data through the hooked model to get the hook outputs.
        # Since the hooked model is the same for all the monitored models, we can use
        # the first monitored model to get the hook outputs.
        hooked_model = next(iter(self.monitored_models.values())).hooked_model
        hooked_model_outputs = hooked_model.predict(fit_data)

        # Fit the model monitors on the hook outputs.
        for monitored_model in self.monitored_models.values():
            monitored_model.fit_on_precomputed_outputs(hooked_model_outputs)

    def predict(
        self,
        in_distribution_data: dict[str, NDArray[np.float32]],
        out_of_distribution_data: dict[str, NDArray[np.float32]],
    ) -> BenchmarkResult:
        """Run the predict step of the monitored models on the in-distribution and
        out-of-distribution data.


        Parameters
        ----------
        in_distribution_data
            Dict containing the in-distribution validation data to use for the benchmark.
            The keys are the names of the in-distribution datasets and the values are the
            corresponding data arrays.
        out_of_distribution_data
            Dict containing out-of-distribution data to use for the benchmark. The keys
            are the names of the out-of-distribution datasets and the values are the
            corresponding data arrays.

        Returns
        -------
        BenchmarkResult
            The benchmark result containing the monitored model outputs on the
            in-distribution and out-of-distribution data.

        Raises
        ------
        ValueError
            If any of the monitored models are not fitted.

        """

        self.check_fitted()

        # Get the monitored model outputs on the in-distribution data.
        in_distribution_data_outputs = {
            model_monitor_id: self._single_monitored_model_predict(
                model_monitor_id, in_distribution_data
            )
            for model_monitor_id in self.monitored_models.keys()
        }

        # Get the monitored model outputs on the out-of-distribution data.
        out_of_distribution_data_outputs = {
            model_monitor_id: self._single_monitored_model_predict(
                model_monitor_id, out_of_distribution_data
            )
            for model_monitor_id in self.monitored_models.keys()
        }

        return BenchmarkResult(
            in_distribution_data_outputs, out_of_distribution_data_outputs
        )

    def check_fitted(self):
        """Check if all monitored models in the benchmark are fitted.

        Raises
        ------
        ValueError
            If any of the monitored models are not fitted.

        """

        for monitored_model in self.monitored_models.values():
            monitored_model.check_fitted()

    def _single_monitored_model_predict(
        self, model_monitor_id: str, data: dict[str, NDArray[np.float32]]
    ) -> dict[str, MonitoredModelOutput]:
        """Run predict on a single monitored model for all the provided datasets.

        Parameters
        ----------
        model_monitor_id
            The identifier of the monitored model to run predict on.
        data
            The datasets to run the monitored model's predict step on.

        Returns
        -------
        dict[str, MonitoredModelOutput]
            Dict containing the monitored model outputs on eacg given dataset. The keys
            are the names of the datasets and the values are the corresponding monitored
            model outputs.

        """

        return {
            data_id: self.monitored_models[model_monitor_id].predict(dataset)
            for data_id, dataset in data.items()
        }

    def evaluate(
        self,
        benchmark_result: BenchmarkResult,
        evaluators: list[Evaluator] = [],
    ):
        """Evaluate the monitored model outputs using the provided evaluators.

        Parameters
        ----------
        benchmark_result
            The benchmark result containing the monitored model outputs on the
            in-distribution and out-of-distribution data.
        evaluators, optional
            List of evaluators to use for evaluating the monitored model outputs.

        """
        pass
