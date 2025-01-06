import numpy as np
import plotly.graph_objects as go  # type: ignore
from numpy.typing import NDArray
from plotly.subplots import make_subplots  # type: ignore

from modelguard.components import BenchmarkResult, MonitoredModelOutput
from modelguard.evaluators.evaluator import Evaluator


class EncompassedMonitorOutputEvaluator(Evaluator):
    """Class to run an encompassed monitor output evaluation on benchmark results.

    This evaluator calculates the percentage of model monitor output scores for
    OOD samples that are that are within the range of model monitor output scores for ID
    samples. This percentage is calculated for each monitored model and ID to OOD
    dataset pair in the benchmark result. The formula for the percentage is:

    .. math::

        encompassed points = \frac{# OOD sample monitor outputs within ID sample score range}
        {# OOD sample monitor outputs}

    Attributes
    ----------
    benchmark_result
        The benchmark result for which to calculate the encompassed monitor output
        scores.
    encompassed_monitor_output_scores
        The encompassed monitor output scores for each monitored model and ID-OOD dataset
        couple. The data structure to store the encompassed monitor output scores is a
        three level dictionary. The first dictionary maps the monitored model identifiers,
        the second dictionary maps the ID dataset names, and the third dictionary maps the
        OOD dataset names to the encompassed monitor output scores for that ID-OOD dataset
        and monitored model, i.e.,
        encompassed_monitor_output_scores[monitored_model_id][id_dataset_name][ood_dataset_name].



    """

    def __init__(self, benchmark_result: BenchmarkResult):
        """Initialize the encompassed monitor output evaluator with a benchmark result.

        Attributes
        ----------
        benchmark_result
            The benchmark result for which to calculate the encompassed monitor output
            scores.

        """
        self.benchmark_result = benchmark_result

    def run(self):
        """Run the encompassed monitor output evaluation on the benchmark result.

        This method calculates the encompassed monitor output scores for each monitored
        model and ID-OOD dataset couple in the benchmark result.

        """

        self.encompassed_monitor_output_scores: dict[
            str, dict[str, dict[str, float]]
        ] = {}

        for monitored_model_id in self.benchmark_result.get_monitored_model_id_keys():
            id_data_outputs_dict, ood_data_outputs_dict = (
                self.benchmark_result.get_monitored_model_results(monitored_model_id)
            )

            self.encompassed_monitor_output_scores[monitored_model_id] = (
                self._single_monitored_model_encompassed_monitor_output_evaluator_run(
                    id_data_outputs_dict, ood_data_outputs_dict
                )
            )

    def _single_monitored_model_encompassed_monitor_output_evaluator_run(
        self,
        id_data_outputs_dict: dict[str, MonitoredModelOutput],
        ood_data_outputs_dict: dict[str, MonitoredModelOutput],
    ) -> dict[str, dict[str, float]]:
        """Run the encompassed monitor output evaluation on the benchmark results for a
        single monitored model.

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
        dict[str, dict[str, float]]
            The encompassed monitor output scores produced by the monitored model for
            each ID-OOD dataset couple. The first dictionary maps the ID dataset name
            and the second dictionary maps the OOD dataset name to the encompassed
            monitor output score for that ID-OOD dataset couple, i.e.,
            encompassed_monitor_output_scores[id_dataset_name][ood_dataset_name].

        """

        encompassed_monitor_output_scores: dict[str, dict[str, float]] = {}

        # For each model monitor output result on an ID dataset, calculate the
        # encompassed monitor output score for that ID dataset with each OOD dataset
        for id_dataset_name, id_data_output in id_data_outputs_dict.items():
            encompassed_monitor_output_scores[id_dataset_name] = {}

            for ood_dataset_name, ood_data_output in ood_data_outputs_dict.items():
                encompassed_monitor_output_scores[id_dataset_name][ood_dataset_name] = (
                    self._calculate_encompassed_sample_monitor_output_score(
                        id_data_output.model_monitor_outputs,
                        ood_data_output.model_monitor_outputs,
                    )
                )

        return encompassed_monitor_output_scores

    def _calculate_encompassed_sample_monitor_output_score(
        self, id_scores: NDArray[np.float32], ood_scores: NDArray[np.float32]
    ):
        """Calculate the encompassed monitor output score for a single ID-OOD dataset
        pair's monitor output scores.

        Parameters
        ----------
        id_scores
            The model monitor output scores for the in-distribution samples.
        ood_scores
            The model monitor output scores for the out-of-distribution samples.

        Returns
        -------
        float
            The percentage of OOD sample monitor output scores that are within the range of
            ID sample monitor output scores.

        """

        # Calculate the range of the ID sample monitor output scores
        id_score_min = id_scores.min()
        id_score_max = id_scores.max()

        # Find the number of OOD sample monitor output scores that are within the range
        # of the ID sample monitor output scores
        encompassed_points = (
            (ood_scores >= id_score_min) & (ood_scores <= id_score_max)
        ).sum()

        # Calculate the percentage of OOD sample monitor output scores that are within
        # the range of the ID sample monitor output scores
        encompassed_points_percentage = encompassed_points / len(ood_scores)

        return encompassed_points_percentage

    def visualize(self) -> go.Figure:
        """Visualize the encompassed monitor output scores for the benchmark result.

        The colorscale of the heatmap visualization is blue to red, with blue indicating
        a lower encompassed monitor output score and red indicating a higher encompassed
        monitor output score. The main information to look for in this heatmap are red
        squares, which indicate that the model monitor output scores for the OOD samples
        are within the range of the model monitor output scores for the ID samples. The
        higher the encompassed monitor output score, the higher the score overlap between
        the ID and OOD samples.

        Returns
        -------
        go.Figure
            The heatmap visualization of the encompassed monitor output scores for the
            ID-OOD dataset couples in the benchmark result.
        """

        # Get the names of the monitored models contained in the results
        monitored_model_names = list(self.encompassed_monitor_output_scores.keys())

        # Create a figure with subplots for each monitored model
        fig = make_subplots(
            rows=len(monitored_model_names),
            cols=1,
            subplot_titles=monitored_model_names,
        )

        for (
            i,
            monitor_encompassed_monitor_output_scores,
        ) in enumerate(self.encompassed_monitor_output_scores.values()):
            id_dataset_names = list(monitor_encompassed_monitor_output_scores.keys())
            ood_dataset_names = list(
                monitor_encompassed_monitor_output_scores[id_dataset_names[0]].keys()
            )

            # Create a matrix of the encompassed monitor output scores
            encompassed_monitor_output_scores = [
                [
                    monitor_encompassed_monitor_output_scores[id_dataset_name][
                        ood_dataset_name
                    ]
                    for ood_dataset_name in ood_dataset_names
                ]
                for id_dataset_name in id_dataset_names
            ]

            fig.add_trace(  # type: ignore
                go.Heatmap(
                    z=encompassed_monitor_output_scores,
                    x=ood_dataset_names,
                    y=id_dataset_names,
                    colorscale="RdBu",
                    reversescale=True,
                    zmin=0,
                    zmax=1,
                    hovertemplate="ID Dataset: %{y}<br>OOD Dataset: %{x}<br>Encompassed monitor output score: %{z:.4f}",
                    texttemplate="%{z:.4f}",
                ),
                row=i + 1,
                col=1,
            )

        return fig
