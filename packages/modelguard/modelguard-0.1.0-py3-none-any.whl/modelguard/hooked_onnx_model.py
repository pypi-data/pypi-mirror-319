from numpy.typing import NDArray
import onnx
from onnx import helper
import onnxruntime as ort  # type: ignore
from modelguard.components.hooked_model_output import HookedModelOutput
from onnxruntime.capi.onnxruntime_pybind11_state import InvalidArgument  # type: ignore
from modelguard.utils import add_batch_dimension
import numpy as np
from typing import cast


class HookedONNXModel:
    """A wrapper class for an ONNX model that adds the ability to log intermediate
    model tensor values during inference using hooks.

    Attributes
    ----------
    model
        The ONNX model to wrap.
    hooks_config
        A dictionary containing both the user defined hook names and the names of the
        ValueInfoProto object referencing the intermediate tensors in the model we want
        to log using hooks. This is in the format of {hook_name: value_info_proto_name}.

    """

    def __init__(self, model: onnx.ModelProto, hooks_config: dict[str, str]):
        """
        Initialize the HookedONNXModel.

        Parameters
        ----------
        model
            The ONNX model to wrap.
        hooks_config
            A dictionary containing both the user defined hook names and the names of
            the ValueInfoProto object referencing the intermediate tensors in the model
            we want to log using hooks. This is in the format of
            `{hook_name: value_info_proto_name}`.

            A ValueInfoProto is an object in the ONNX graph that defines an
            intermediate input or output tensor in the model. These can be found by
            visualizing the ONNX graph using for example
            :ref:`NETRON <https://netron.app/>`.

            Note: By default, we also log the model input and output, so there is no need
            to specify these as hooks in this config.

        Raises
        ------
        ValueError
            If the ONNXRuntime InferenceSession cannot be initialized for the model.

        """

        self.model = model
        self.hooks_config = hooks_config
        self._add_hooks()

        try:
            self._initialize_inference_session()
        except InvalidArgument as e:  # type: ignore
            raise ValueError(
                "Failed to initialize ONNXRuntime InferenceSession for the new HookedONNXModel. "
            ) from e

    def _add_hooks(self):
        """
        Add hooks to the model which capture requested intermediate model tensor
        values during inference.
        """

        # For each hook we want to add, build a new ValueInfoProto object with the same
        # name of the already existing ValueInfoProto tensor in the model's GraphProto
        # referencing the intermediate tensor we want to log.
        hook_value_info_protos = []
        for value_info_proto_name in self.hooks_config.values():
            value_info_proto = helper.ValueInfoProto()  # type: ignore
            value_info_proto.name = value_info_proto_name
            hook_value_info_protos.append(value_info_proto)  # type: ignore

        # Add our created ValueInfoProtos to the model's graph output. By doing this, we
        # change the output of our ONNX graph so that it also outputs the values
        # contained in the intermediate tensors referenced by these ValueInfoProto
        # objects we created (in addition to the normal model output).
        self.model.graph.output.extend(hook_value_info_protos)  # type: ignore

    def _initialize_inference_session(self):
        self._inference_session = ort.InferenceSession(self.model.SerializeToString())

    def predict(self, x: NDArray[np.float32]) -> HookedModelOutput:
        """Run the hooked model on input sample(s).

        Parameters
        ----------
        x
            The input sample(s) to run inference on. The first dimension of the provided
            numpy array should always correspond to the batch dimension, even if the
            input is a single sample.


        Returns
        -------
        HookedModelOutput
            A HookedModelOutput object containing the model's input and output tensors
            as well as the tensors of the intermediate model activations logged using
            hooks.
        """

        return HookedModelOutput.from_hooked_model_output_list(
            [self._run_hooked_single_sample_inference(x_sample) for x_sample in x]
        )

    def _run_hooked_single_sample_inference(
        self, input_sample: NDArray[np.float32]
    ) -> HookedModelOutput:
        """Run inference on the model for a single input sample while logging the values
        of the intermediate tensors configured as hooks.

        Parameters
        ----------
        input_sample : NDArray
            The input sample to pass to the model for inference.

        Returns
        -------
        HookedModelOutput
            A HookedModelOutput object containing the model's input and output tensors
            as well as the tensors of the intermediate model activations logged using
            hooks.
        """

        # Add a batch dimension to the single sample
        input_sample = add_batch_dimension(input_sample)

        # Add the input sample to the model output dict
        model_output_dict = {"input": input_sample}

        # Run inference of the model
        # Note: 'x' is the registered model input and [] means that we want to capture
        # all model outputs (i.e. the normal model output and the added hooks outputs)
        model_outputs: list[NDArray[np.float32]] = cast(
            list[NDArray[np.float32]],
            self._inference_session.run([], {"x": input_sample}),  # type: ignore
        )

        # The model outputs are returned as a list of numpy arrays with the ordering
        # starting with the regular model output followed by the hooked outputs. The
        # order of the hooked outputs is the same as the order in which they were added,
        # i.e. the same order as the entries in the hooks_config dict. Based on this
        # ordering we create a dict to reference them.
        model_output_dict["output"] = model_outputs[0]
        for hook_user_name, model_output in zip(
            self.hooks_config.keys(), model_outputs[1:]
        ):
            model_output_dict[hook_user_name] = model_output

        return HookedModelOutput(model_output_dict)
