import numpy as np
from plotly.graph_objs import Figure, Heatmap
from plotly.subplots import make_subplots
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from modelguard.components import BenchmarkResult, MonitoredModelOutput
from modelguard.evaluators.evaluator import Evaluator


class OODProbabilityEvaluationMetricsEvaluator(Evaluator):
    """Class to run an OOD probability evaluation metrics evaluator on benchmark results.

    This evaluator calculates a number of classification performance evaluation
    metrics for the predicted OOD scores of the samples in a benchmark result.

    The evaluation metrics that will be calculated are:
    - Accuracy
    - F1-Score
    - Precision
    - Recall
    - AUC of the ROC

    Attributes
    ----------
    benchmark_result
        The benchmark result for which to calculate the OOD probability evaluation
        metrics.
    ood_probability_evaluation_mectrics
        The OOD probability evaluation metric scores for each monitored model. This is
        stored in a two dimensional dictionary. The first dictionary maps the monitored
        model identifiers and the second dictionary maps the specific evaluation metric
        type to the corresponding metric score, i.e.,
        ood_probability_evaluation_mectrics[monitored_model_id][evaluation_metric].

    """

    def __init__(self, benchmark_result: BenchmarkResult):
        """Initialize the OOD probability evaluation metric evaluator with a benchmark
        result.

        Parameters
        ----------
        benchmark_result
            The benchmark result for which to calculate OOD probability confusion
            matrix.

        """
        self.benchmark_result = benchmark_result
        self.ood_probability_evaluation_mectrics = {}

    def run(self):
        """Run the OOD probability evaluation metric evaluator.

        This method calculates the evaluation metric scores for the predicted OOD scores
        of the samples in a benchmark result.

        """

        for monitored_model_id in self.benchmark_result.get_monitored_model_id_keys():
            id_data_outputs_dict, ood_data_outputs_dict = (
                self.benchmark_result.get_monitored_model_results(monitored_model_id)
            )

            self.ood_probability_evaluation_mectrics[monitored_model_id] = (
                self._single_monitored_model_ood_probability_evaluation_metric_evaluator_run(
                    id_data_outputs_dict, ood_data_outputs_dict
                )
            )

    def _single_monitored_model_ood_probability_evaluation_metric_evaluator_run(
        self,
        id_data_outputs_dict: dict[str, MonitoredModelOutput],
        ood_data_outputs_dict: dict[str, MonitoredModelOutput],
    ) -> dict[str, float]:
        """Run the OOD probability evaluation metrics evaluator on the benchmark results
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
        dict[str, float]
            The OOD probability evaluation metric scores by the monitored model. The
            dictionary maps the specific evaluation metric type to the corresponding
            metric score, i.e., ood_probability_evaluation_mectrics[evaluation_metric].

        """

        ood_probability_evaluation_mectrics: dict[str, float] = {}

        # Collect all monitor OOD prob outputs for the ID data
        id_data_ood_probs = np.array([])
        for id_data_outputs in id_data_outputs_dict.values():
            id_data_ood_probs = np.concatenate(
                (id_data_ood_probs, id_data_outputs.post_processor_outputs), axis=0
            )

        # Collect all monitor OOD prob outputs for the OOD data
        ood_data_ood_probs = np.array([])
        for ood_data_outputs in ood_data_outputs_dict.values():
            ood_data_ood_probs = np.concatenate(
                (ood_data_ood_probs, ood_data_outputs.post_processor_outputs), axis=0
            )

        # Combine all data OOD prob outputs
        ood_probs = np.concatenate((id_data_ood_probs, ood_data_ood_probs), axis=0)

        # Create a ground truth array that contains the correct binary classifications
        # for each corresponding sample in the monitored model's OOD prob array.
        targets = np.concatenate(
            (np.zeros_like(id_data_ood_probs), np.ones_like(ood_data_ood_probs)), axis=0
        )

        # Create an array of the predicted binary classes from the OOD prob outputs
        # (Some metrics require this)
        ood_preds = np.where(ood_probs > 0.5, 1, 0)

        # Calculate the evaluation metric scores
        ood_probability_evaluation_mectrics["accuracy"] = accuracy_score(
            targets, ood_preds
        )
        ood_probability_evaluation_mectrics["f1"] = f1_score(targets, ood_preds)
        ood_probability_evaluation_mectrics["recall"] = recall_score(targets, ood_preds)
        ood_probability_evaluation_mectrics["precision"] = precision_score(
            targets, ood_preds
        )
        ood_probability_evaluation_mectrics["roc_auc"] = roc_auc_score(
            targets, ood_probs
        )

        return ood_probability_evaluation_mectrics

    def visualize(self) -> Figure:
        """Visualize the OOD probability evaluation metric scores on the benchmark
        results.

        Returns
        -------
        Figure
            The heatmap of the OOD probability evaluation metric scores on the benchmark
            results.
        """

        # Get the names of the monitored models contained in the results
        monitored_model_names = list(self.ood_probability_evaluation_mectrics.keys())

        # Create a figure with subplots for each monitored model
        fig = make_subplots(
            rows=len(monitored_model_names),
            cols=1,
            subplot_titles=monitored_model_names,
        )

        for (
            i,
            monitor_ood_probability_evaluation_metrics,
        ) in enumerate(self.ood_probability_evaluation_mectrics.values()):

            metric_ids = list(monitor_ood_probability_evaluation_metrics.keys())
            metric_scores = [list(monitor_ood_probability_evaluation_metrics.values())]

            fig.add_trace(  # type: ignore
                Heatmap(
                    z=metric_scores,
                    x=metric_ids,
                    colorscale="Blues",
                    zmin=0,
                    zmax=1,
                    reversescale=False,
                    hovertemplate="Metric: %{x}<br>Score: %{z:.4f}",
                    texttemplate="%{z:.4f}",
                ),
                row=i + 1,
                col=1,
            )

            fig.update_xaxes({"title": "OOD Probability Evaluation Metric Scores"})
            fig.update_yaxes({"showticklabels": False})

        return fig
