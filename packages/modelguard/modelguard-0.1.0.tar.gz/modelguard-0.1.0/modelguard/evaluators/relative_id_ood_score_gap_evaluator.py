from modelguard.components import BenchmarkResult, MonitoredModelOutput
from modelguard.evaluators.evaluator import Evaluator
import plotly.graph_objects as go  # type: ignore
from plotly.subplots import make_subplots  # type: ignore
from numpy.typing import NDArray
import numpy as np


class RelativeIDOODScoreGapEvaluator(Evaluator):
    """Class to run a relative ID-OOD score gap evaluation on benchmark results.

    One characteristic all monitoring techniques should have is that there
    should be a gap between the monitor output scores for ID and OOD samples.
    Ideally, this ID-OOD gap should be as large as possible to more easily
    distinguish OOD samples.

    To account for the different magnitudes of the different monitoring techniques,
    we need to normalise these scores to make them comparable across techniques. To
    this end, we can measure the relative score gap between a ID-OOD dataset couples
    using the following formula:

    .. math::

        relative gap = \frac{max(ID scores) - min(OOD scores)}{max(ID scores) - min(ID scores)}

    > Important: The calculations behind the relative ID-OOD score gap are based on the
    assumption that the model monitor outputs are high for OOD samples and low for ID
    samples. If the model monitor outputs are low for OOD samples and high for ID
    samples, the relative ID-OOD score gap evaluation will not work as intended.

    Attributes
    ----------
    benchmark_result
        The benchmark result for which to calculate the relative ID-OOD score gaps.
    relative_id_ood_score_gaps
        The relative ID-OOD score gaps for each monitored model and ID-OOD dataset
        couple. The data structure to store the relative ID-OOD score gaps is a three
        level dictionary. The first dictionary maps the monitored model identifiers, the
        second dictionary maps the ID dataset names, and the third dictionary maps the
        OOD dataset names to the relative ID-OOD score gaps for that ID-OOD dataset and
        monitored model, i.e.,
        relative_id_ood_score_gaps[monitored_model_id][id_dataset_name][ood_dataset_name].

    """

    def __init__(self, benchmark_result: BenchmarkResult):
        """Initialize the relative ID-OOD score gap evaluator with a benchmark result.

        Parameters
        ----------
        benchmark_result
            The benchmark result for which to calculate the relative ID-OOD score gaps.

        """

        self.benchmark_result = benchmark_result

    def run(self):
        """Run the relative ID-OOD score gap evaluation on the benchmark result.

        This method calculates the relative ID-OOD score gap for each monitored model
        and ID-OOD dataset couple in the benchmark result.

        """

        self.relative_id_ood_score_gaps: dict[str, dict[str, dict[str, float]]] = {}

        for monitored_model_id in self.benchmark_result.get_monitored_model_id_keys():
            id_data_outputs_dict, ood_data_outputs_dict = (
                self.benchmark_result.get_monitored_model_results(monitored_model_id)
            )

            self.relative_id_ood_score_gaps[monitored_model_id] = (
                self._single_monitored_model_relative_id_ood_score_gap_test(
                    id_data_outputs_dict, ood_data_outputs_dict
                )
            )

    def _single_monitored_model_relative_id_ood_score_gap_test(
        self,
        id_data_outputs_dict: dict[str, MonitoredModelOutput],
        ood_data_outputs_dict: dict[str, MonitoredModelOutput],
    ) -> dict[str, dict[str, float]]:
        """Run the relative ID-OOD score gap evaluation on the benchmark results for a
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
            The relative ID-OOD score gaps produced by the monitored model for each
            ID-OOD dataset couple. The first dictionary maps the ID dataset names to the
            relative ID-OOD score gaps for that ID dataset. The second dictionary then
            maps the OOD dataset names to the relative ID-OOD score gaps for that OOD
            dataset, i.e.,
            relative_id_ood_score_gaps[id_dataset_name][ood_dataset_name].

        """

        relative_id_ood_score_gaps: dict[str, dict[str, float]] = {}

        # For each model monitor output result on an ID dataset, calculate the
        # relative ID-OOD score gap with each model monitor output result on an OOD
        # dataset
        for (
            id_dataset_name,
            id_outputs,
        ) in id_data_outputs_dict.items():
            relative_id_ood_score_gaps[id_dataset_name] = {}

            # For each model monitor output result on an OOD dataset, calculate the
            for (
                ood_dataset_name,
                ood_outputs,
            ) in ood_data_outputs_dict.items():
                relative_id_ood_score_gaps[id_dataset_name][ood_dataset_name] = (
                    self._calculate_relative_id_ood_score_gap(
                        id_outputs.model_monitor_outputs,
                        ood_outputs.model_monitor_outputs,
                    )
                )

        return relative_id_ood_score_gaps

    def _calculate_relative_id_ood_score_gap(
        self, id_scores: NDArray[np.float32], ood_scores: NDArray[np.float32]
    ) -> float:
        """Calculate the relative ID-OOD score gap between the ID and OOD scores.

        Parameters
        ----------
        id_scores
            The scores of the monitored model on an in-distribution dataset.
        ood_scores
            The scores of the monitored model on an out-of-distribution dataset.

        Returns
        -------
        float
            The relative ID-OOD score gap between the ID and OOD scores.

        """

        # Calculate the required ID score statistics
        min_id_score = min(id_scores)
        max_id_score = max(id_scores)

        # Calculate the needed OOD score statistics
        min_ood_score = min(ood_scores)

        # Calculate the relative ID-OOD score gap
        relative_gap = float(
            (min_ood_score - max_id_score) / (max_id_score - min_id_score)
            if (max_id_score - min_id_score) != 0
            else 0.0
        )

        return relative_gap

    def visualize(self) -> go.Figure:
        """Visualize the relative ID-OOD score gaps as a heatmap.

        The color range of the heatmap is from red to blue, where red indicates a
        relative ID-OOD score gap of 0 and blue indicates a relative ID-OOD score gap of
        1. The main information to look for in this heatmap are red squares, which
        indicate a low or even negative relative ID-OOD score gap.

        Returns
        -------
        go.Figure
            The heatmap visualisation of the relative ID-OOD score gaps.

        """

        # Get the names of the monitored models contained in the results
        monitored_model_names = list(self.relative_id_ood_score_gaps.keys())

        # Create a figure with subplots for each monitored model
        fig = make_subplots(
            rows=len(monitored_model_names),
            cols=1,
            subplot_titles=monitored_model_names,
        )

        for (
            i,
            monitor_relative_id_ood_score_gaps,
        ) in enumerate(self.relative_id_ood_score_gaps.values()):

            # Get the names of the ID and OOD datasets
            id_dataset_names = list(monitor_relative_id_ood_score_gaps.keys())
            ood_dataset_names = list(
                monitor_relative_id_ood_score_gaps[id_dataset_names[0]].keys()
            )

            # Create a matrix of the relative ID-OOD score gaps
            relative_id_ood_score_gap_matrix = [
                [
                    monitor_relative_id_ood_score_gaps[id_dataset_name][
                        ood_dataset_name
                    ]
                    for ood_dataset_name in ood_dataset_names
                ]
                for id_dataset_name in id_dataset_names
            ]

            # Create a heatmap for the relative ID-OOD score gaps
            fig.add_trace(  # type: ignore
                go.Heatmap(
                    z=relative_id_ood_score_gap_matrix,
                    x=ood_dataset_names,
                    y=id_dataset_names,
                    zmin=0,
                    zmax=1,
                    colorscale="RdBu",
                    hovertemplate="ID Dataset: %{y}<br>OOD Dataset: %{x}<br>Relative ID-OOD score gap: %{z:.4f}",
                    texttemplate="%{z:.4f}",
                ),
                row=i + 1,
                col=1,
            )

        return fig
