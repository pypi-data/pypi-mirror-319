import numpy as np
from numpy.typing import NDArray

from modelguard.components import HookedModelOutput, MonitoredModelOutput
from modelguard.hooked_onnx_model import HookedONNXModel
from modelguard.model_monitors import ModelMonitor
from modelguard.post_processors import PostProcessor


class MonitoredModel:
    def __init__(
        self,
        hooked_model: HookedONNXModel,
        model_monitor: ModelMonitor,
        post_processor: PostProcessor,
    ):
        """Initialize a MonitoredModel instance.

        Parameters
        ----------
        hooked_model
            The hooked model instance to monitor.
        model_monitor
            The model monitor instance to use for monitoring the hooked model.
        post_processor
            The post-processor instance to use for post-processing the model monitor
            outputs. The default is a pass-through post-processor that returns the
            monitor scores as is.

        Raises
        ------
        ValueError
            If any of the required hooks for the chosen model monitoring technique are
            not available in the hooked model.
        """

        self.hooked_model = hooked_model
        self.model_monitor = model_monitor
        self.post_processor = post_processor

        self._check_required_hooks_availability()

    def _check_required_hooks_availability(self):
        """Check if the required hooks of the model monitor are available in the hooked
        model.

        Raises
        ------
        ValueError
            If any of the required hooks are not available in the hooked model.
        """

        required_hooks = set(self.model_monitor.required_model_hooks)

        # Remove the "input" and "output" hooks from the required hooks list, as they
        # are always available in the model.
        required_hooks.discard("input")
        required_hooks.discard("output")

        # Check if all the required hooks are available in the hooked model.
        missing_hooks = required_hooks - set(self.hooked_model.hooks_config.keys())

        if missing_hooks:
            raise ValueError(
                f"Model is missing the following required hooks: {missing_hooks}"
            )

    def fit(self, fit_data: NDArray[np.float32]):
        """Fit the model monitor on the hook outputs of the contained model based on the
        given data.

        This fitting step first sends the fit data through the hooked model to get the
        hook outputs. Then, the model monitor is fitted on these hook outputs.

        Parameters
        ----------
        fit_data
            The data to fit the model / monitor duo on. This fit data should represent
            the original model's training data to ensure that the model monitor is
            conditioned on the "normal" model state.

            The first dimension of the provided numpy array should always correspond to
            the batch dimension, even if the input is a single sample. All elements in
            the input array be of dtype float32.
        """

        # TODO: Add logging

        # Get the monitored model's outputs based on the fit data.
        hooked_model_output = self.hooked_model.predict(fit_data)

        # Fit the model monitor on the hooked model outputs.
        self.model_monitor.fit(hooked_model_output)

        # Send the fit data through the model monitor to gather the monitor scores.
        fit_data_model_monitor_outputs = self.model_monitor.predict(hooked_model_output)

        # Fit the post-processor on the monitor scores.
        self.post_processor.fit(fit_data_model_monitor_outputs)

    def fit_on_precomputed_outputs(self, hooked_model_output: HookedModelOutput):
        """Fit the model monitor on a precomputed hooked model output.

        This fitting step fits the model monitor on the precomputed hooked model
        outputs of the contained model if the hook outputs are already available.

        Parameters
        ----------
        hooked_model_output
            The precomputed hooked model outputs to fit the model monitor on.
        """

        # Fit the model monitor on the precomputed hooked model outputs.
        self.model_monitor.fit(hooked_model_output)

        # Send the precomputed hooked model outputs through the model monitor to gather
        # the monitor scores.
        model_monitor_outputs = self.model_monitor.predict(hooked_model_output)

        # Fit the post-processor on the monitor scores.
        self.post_processor.fit(model_monitor_outputs)

    def check_fitted(self):
        """Check if the monitored model is fitted.

        Check if the monitored model is fitted by checking if the monitored model's
        model monitor and post-processor are fitted.

        Raises
        ------
        ValueError
            If the monitored model is not fitted.
        """

        self.model_monitor.check_fitted()
        self.post_processor.check_fitted()

    def predict(self, x: NDArray[np.float32]) -> MonitoredModelOutput:
        """Make predictions on the input data

        Parameters
        ----------
        x
            The input data to make predictions on. The first dimension of the provided
            numpy array should always correspond to the batch dimension, even if the
            input is a single sample. All elements in the input array be of dtype
            float32.

        Returns
        -------
        MonitoredModelOutput
            The predictions made by the hooked model (output only) and model monitor.

        Raises
        ------
        ValueError
            If the monitored model is not fitted.

        """

        # TODO: Add logging

        self.check_fitted()

        # Get the hooked model outputs based on the input data.
        hooked_model_outputs = self.hooked_model.predict(x)

        # Make predictions using the model monitor.
        model_monitor_predictions = self.model_monitor.predict(hooked_model_outputs)

        # Post-process the model monitor predictions.
        post_processor_predictions = self.post_processor.predict(
            model_monitor_predictions
        )

        return MonitoredModelOutput(
            hooked_model_outputs["output"],
            model_monitor_predictions,
            post_processor_predictions,
        )
