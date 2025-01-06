import numpy as np
from plotly.graph_objs import Figure, Heatmap  # type: ignore
from plotly.subplots import make_subplots  # type: ignore

from modelguard.components import BenchmarkResult, MonitoredModelOutput
from modelguard.evaluators.evaluator import Evaluator


class OODProbabilityConfusionMatrixEvaluator(Evaluator):
    """Class to run an OOD probability confusion matrix evaluator on benchmark results

    This evaluator calculates the confusion matrix for the predicted OOD scores of the
    samples in a benchmark result.

    Attributes
    ----------
    benchmark_result
        The benchmark result for which to calculate the OOD probability confusion matrix.
    ood_probability_confusion_matrices
        The OOD probability confusion scores produced by each monitored model. This is
        stored in a three dimensional dictionary. The first dictionary maps the
        monitored model identifiers, the second dictionary maps the actual ID/OOD
        classes and the second third maps the predicted ID/OOD classes to the confusion
        values, i.e.,
        ood_probability_confusion_matrix[monitored_model_id][actual_idood_class][pred_idood_class].
        The possible keys for both the actual and predicted ID/OOD classes are both `id`
        and `ood`.


    """

    def __init__(self, benchmark_result: BenchmarkResult):
        """Initialize the OOD probability confusion matrix evaluator with a benchmark
        result.

        Parameters
        ----------
        benchmark_result
            The benchmark result for which to calculate OOD probability confusion
            matrix.

        """
        self.benchmark_result = benchmark_result
        self.ood_probability_confusion_matrices = {}

    def run(self):
        """Run the OOD probability confusion matrix evaluator.

        This method calculates the confusion matrix for the predicted OOD scores of the
        samples in a benchmark result.

        """

        for monitored_model_id in self.benchmark_result.get_monitored_model_id_keys():
            id_data_outputs_dict, ood_data_outputs_dict = (
                self.benchmark_result.get_monitored_model_results(monitored_model_id)
            )

            self.ood_probability_confusion_matrices[monitored_model_id] = (
                self._single_monitored_model_ood_probability_confusion_matrix_evaluator_run(
                    id_data_outputs_dict, ood_data_outputs_dict
                )
            )

    def _single_monitored_model_ood_probability_confusion_matrix_evaluator_run(
        self,
        id_data_outputs_dict: dict[str, MonitoredModelOutput],
        ood_data_outputs_dict: dict[str, MonitoredModelOutput],
    ) -> dict[str, dict[str, int]]:
        """Run the OOD probability confusion matrix evaluator on the benchmark results
        for a single monitored model.

        Parameters
        ----------
        id_data_outputs_dict
            The outputs of the monitored model on the in-distribution data. The
            dictionary maps the dataset names to the outputs of the monitored model on
            that dataset.
        ood_data_outputs_dict
            The outputs of the monitored model on the out-of-distribution data. The
            dictionary maps the dataset names to the outputs of the monitored model on
            that dataset.

        Returns
        -------
        dict[str, dict[str, int]]
            The OOD probability confusion scores produced by the monitored model. The
            first dictionary maps the actual ID/OOD classifications and the second
            dictionary maps the predicted ID/OOD classifications to the confusion
            values, i.e.,
            ood_probability_confusion_matrix[actual_idood_class][pred_idood_class].
            The possible keys for both the actual and predicted ID/OOD classifications
            are both `id` and `ood`.

        """

        ood_probability_confusion_matrix: dict[str, dict[str, int]] = {}

        # Count the number of samples in the actual ID datasets that have been predicted
        # as ID and OOD
        ood_probability_confusion_matrix["id"] = {"id": 0, "ood": 0}
        for id_data_outputs in id_data_outputs_dict.values():
            id_data_pred_id = np.count_nonzero(
                id_data_outputs.post_processor_outputs <= 0.5
            )
            id_data_pred_ood = (
                len(id_data_outputs.post_processor_outputs) - id_data_pred_id
            )

            ood_probability_confusion_matrix["id"]["id"] += id_data_pred_id
            ood_probability_confusion_matrix["id"]["ood"] += id_data_pred_ood

        # Count the number of samples in the actual ID datasets that have been predicted
        # as ID and OOD
        ood_probability_confusion_matrix["ood"] = {"id": 0, "ood": 0}
        for ood_data_outputs in ood_data_outputs_dict.values():
            ood_data_pred_id = np.count_nonzero(
                ood_data_outputs.post_processor_outputs <= 0.5
            )
            ood_data_pred_ood = (
                len(ood_data_outputs.post_processor_outputs) - ood_data_pred_id
            )

            ood_probability_confusion_matrix["ood"]["id"] += ood_data_pred_id
            ood_probability_confusion_matrix["ood"]["ood"] += ood_data_pred_ood

        return ood_probability_confusion_matrix

    def visualize(self) -> Figure:
        """Visualize the OOD probability confusion matrix scores on the benchmark
        results.

        Returns
        -------
        Figure
            The heatmap of the OOD probability confusion matrix scores on the benchmark
            results.
        """

        # Get the names of the monitored models contained in the results
        monitored_model_names = list(self.ood_probability_confusion_matrices.keys())

        # Create a figure with subplots for each monitored model
        fig = make_subplots(
            rows=len(monitored_model_names),
            cols=1,
            subplot_titles=monitored_model_names,
        )

        for (
            i,
            monitor_ood_probability_confusion_matrix,
        ) in enumerate(self.ood_probability_confusion_matrices.values()):

            # Create a confusion matrix of the ood probability confusion scores
            monitor_ood_probability_confusion_scores = [
                [
                    monitor_ood_probability_confusion_matrix[actual_idood_class][
                        predicted_idood_class
                    ]
                    for predicted_idood_class in ["id", "ood"]
                ]
                for actual_idood_class in ["id", "ood"]
            ]

            fig.add_trace(  # type: ignore
                Heatmap(
                    z=monitor_ood_probability_confusion_scores,
                    x=["id", "ood"],
                    y=["id", "ood"],
                    colorscale="Blues",
                    reversescale=False,
                    hovertemplate="Actual class: %{y}<br>Pred class: %{x}<br>Number of samples: %{z:0.0f}",
                    texttemplate="%{z:0.0f}",
                ),
                row=i + 1,
                col=1,
            )

            fig.update_xaxes({"title": "Predicted"})
            fig.update_yaxes({"title": "Actual"})

        return fig
