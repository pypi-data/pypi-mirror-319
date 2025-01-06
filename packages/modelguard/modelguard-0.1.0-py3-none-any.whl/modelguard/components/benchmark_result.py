from modelguard.components import MonitoredModelOutput


class BenchmarkResult:
    """Container class to store the results of a benchmarking run.

    Attributes
    ----------
    in_distribution_data_outputs
        The outputs of the monitored models on the in-distribution data. The first
        dictionary maps the model monitor identifiers to the outputs of that monitored
        model on the in-distribution data. The second dictionary then maps the dataset
        names to the outputs of the monitored model on that dataset, i.e.,
        in_distribution_data_outputs[model_monitor_id][dataset_name].
    out_of_distribution_data_outputs
        The outputs of the monitored models on the out-of-distribution data. The
        first dictionary maps the model monitor identifiers to the outputs of that
        monitored model on the out-of-distribution data. The second dictionary then
        maps the dataset names to the outputs of the monitored model on that dataset,
        i.e., out_of_distribution_data_outputs[model_monitor_id][dataset_name].

    """

    def __init__(
        self,
        in_distribution_data_outputs: dict[str, dict[str, MonitoredModelOutput]],
        out_of_distribution_data_outputs: dict[str, dict[str, MonitoredModelOutput]],
    ):
        """Initialize a BenchmarkResult instance.

        Parameters
        ----------
        in_distribution_data_outputs
            The outputs of the monitored models on the in-distribution data. The first
            dictionary maps the model monitor identifiers to the outputs of that monitored
            model on the in-distribution data. The second dictionary then maps the dataset
            names to the outputs of the monitored model on that dataset, i.e.,
            in_distribution_data_outputs[model_monitor_id][dataset_name].
        out_of_distribution_data_outputs
            The outputs of the monitored models on the out-of-distribution data. The
            first dictionary maps the model monitor identifiers to the outputs of that
            monitored model on the out-of-distribution data. The second dictionary then
            maps the dataset names to the outputs of the monitored model on that dataset,
            i.e., out_of_distribution_data_outputs[model_monitor_id][dataset_name].

        """

        self.in_distribution_data_outputs = in_distribution_data_outputs
        self.out_of_distribution_data_outputs = out_of_distribution_data_outputs

    def get_monitored_model_id_keys(self) -> set[str]:
        """Return the monitored model identifiers in the benchmark results.

        Returns
        -------
        set[str]
            The monitored model identifiers in the benchmark results.

        """

        return set(self.in_distribution_data_outputs.keys())

    def get_monitored_model_results(
        self, monitored_model_id: str
    ) -> tuple[dict[str, MonitoredModelOutput], dict[str, MonitoredModelOutput]]:
        """Return the benchmark results of a specific monitored model for both ID and
        OOD data.

        Parameters
        ----------
        monitored_model_id
            The identifier of the monitored model.

        Returns
        -------
        tuple[dict[str, MonitoredModelOutput], dict[str, MonitoredModelOutput]]
            The benchmark results of the monitored model for both ID and OOD data as
            the first and second element of the tuple, respectively. Each dictionary
            maps the dataset names to the outputs of the monitored model on that
            dataset.

        """

        return (
            self.in_distribution_data_outputs[monitored_model_id],
            self.out_of_distribution_data_outputs[monitored_model_id],
        )
