import plotly.graph_objects as go  # type: ignore
from plotly.subplots import make_subplots  # type: ignore

from modelguard.components import BenchmarkResult
from modelguard.evaluators.evaluator import Evaluator


class MonitorOutputStripPlotEvaluator(Evaluator):
    """Class to run a monitor output strip plot evaluation on benchmark results.

    This evaluator does not calculate any evaluation metrics. Instead, it visualizes
    the monitor outputs of the monitored models on all the ID and OOD datasets in the
    benchmark result in a strip plot.

    Attributes
    ----------
    benchmark_result
        The benchmark result for which to visualize the monitor outputs.

    """

    def __init__(self, benchmark_result: BenchmarkResult):
        """Initialize the monitor output strip plot evaluator with a benchmark result.

        Attributes
        ----------
        benchmark_result
            The benchmark result for which to visualize the monitor outputs.

        """
        self.benchmark_result = benchmark_result

    def run(self):
        """Run the monitor output strip plot evaluation on the benchmark result.

        This method does not calculate any evaluation metrics so it does nothing.

        """
        pass

    def visualize(self) -> go.Figure:
        """Visualize the results of the monitor outputs strip plot evaluation.

        This method creates a strip plot of the monitor outputs of the monitored models
        on all the ID and OOD datasets in the benchmark result. The monitor outputs for
        ID datasets are plotted in blue and the monitor outputs for OOD datasets are
        plotted in red.

        Returns
        -------
        go.Figure
            The strip plot of the monitor outputs of the monitored models on all the ID
            and OOD datasets in the benchmark result.

        """
        # Get the names of the monitored models contained in the benchmark results
        monitored_model_names = list(
            self.benchmark_result.get_monitored_model_id_keys()
        )

        # Create a figure with subplots for each monitored model
        fig = make_subplots(
            rows=len(monitored_model_names),
            cols=1,
            subplot_titles=monitored_model_names,
        )

        for (
            i,
            monitored_model_name,
        ) in enumerate(monitored_model_names):

            # Get the monitor benchmark result for the monitored model
            monitor_benchmark_result = (
                self.benchmark_result.get_monitored_model_results(monitored_model_name)
            )

            # Get the ID and OOD dataset names
            id_dataset_names = list(monitor_benchmark_result[0].keys())
            ood_dataset_names = list(monitor_benchmark_result[1].keys())

            # Reverse the order of the ID and OOD dataset names so that the plot is
            # ordered
            id_dataset_names.reverse()
            ood_dataset_names.reverse()

            # Add all the traces for the OOD datasets
            for ood_dataset_name in ood_dataset_names:
                ood_dataset_monitored_model_outputs = monitor_benchmark_result[1][
                    ood_dataset_name
                ].model_monitor_outputs

                fig.add_trace(  # type: ignore
                    go.Scatter(
                        x=ood_dataset_monitored_model_outputs,
                        y=[ood_dataset_name] * len(ood_dataset_monitored_model_outputs),
                        mode="markers",
                        marker=dict(size=10, opacity=0.1, color="#C7003A"),
                        name=monitored_model_name,
                        showlegend=False,
                    ),
                    row=i + 1,
                    col=1,
                )

            # Add all the traces for the ID datasets
            for id_dataset_name in id_dataset_names:
                id_dataset_monitored_model_outputs = monitor_benchmark_result[0][
                    id_dataset_name
                ].model_monitor_outputs

                fig.add_trace(  # type: ignore
                    go.Scatter(
                        x=id_dataset_monitored_model_outputs,
                        y=[id_dataset_name] * len(id_dataset_monitored_model_outputs),
                        mode="markers",
                        marker=dict(size=10, opacity=0.1, color="#07478F"),
                        name=monitored_model_name,
                        showlegend=False,
                    ),
                    row=i + 1,
                    col=1,
                )

        return fig
