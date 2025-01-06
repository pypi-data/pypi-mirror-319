from numpy.typing import NDArray
import numpy as np


class HookedModelOutput:
    """A container class to store the results of a hooked model's inference on a
    collection of samples.

    The class is used to store the results of the model's inference on a collection of
    samples in a dictionary. The keys of the dictionary are the names of the hooks that
    were used to log the model's output/intermediate tensors during inference. The
    values are numpy arrays containing the model tensors for the passed samples.

    Note that the first dimension of each value numpy array always corresponds to the
    sample index, even if the input sample was a single sample.
    """

    def __init__(
        self,
        hooked_model_inference_results: dict[str, NDArray[np.float32]],
    ):
        """Initialize an inference logging result object.

        Parameters
        ----------
        hooked_model_inference_results
            The data that was logged by the hooks during the model's inference on the
            input samples. The keys are the names of the hooks and the values are the
            corresponding model tensors as numpy arrays.

            We expect the first dimension of the numpy arrays to correspond to the
            sample index, even if the input sample was a single sample.

        """

        self._hooked_model_inference_results = hooked_model_inference_results

    @classmethod
    def from_hooked_model_output_list(
        cls, hooked_model_output_list: list["HookedModelOutput"]
    ) -> "HookedModelOutput":
        """Combine a list of HookedModelOutput objects into a single HookedModelOutput
        object.

        Parameters
        ----------
        hooked_model_output_list
            The list of HookedModelOutput objects to combine.

        Returns
        -------
        HookedModelOutput
            The combined HookedModelOutput object.

        """

        hooks_list = hooked_model_output_list[0].keys()
        combined_hooked_model_inference_results: dict[str, NDArray[np.float32]] = {}

        for hook in hooks_list:
            combined_hooked_model_inference_results[hook] = np.concatenate(
                [
                    hooked_model_output[hook].astype(np.float32)
                    for hooked_model_output in hooked_model_output_list
                ],
                axis=0,
            )

        return cls(combined_hooked_model_inference_results)

    def __getitem__(self, key: str) -> NDArray[np.float32]:
        """Get the data logged by a specific hook.

        Parameters
        ----------
        key : str
            The name of the hook to get the data for.

        Returns
        -------
        NDArray
            The data logged by the hook.

        """
        return self._hooked_model_inference_results[key]

    def __setitem__(self, key: str, value: NDArray[np.float32]):
        """Set the data logged by a specific hook.

        Parameters
        ----------
        key : str
            The name of the hook to set the data for.
        value : NDArray
            The data to set for the hook.

        """
        self._hooked_model_inference_results[key] = value

    def keys(self) -> set[str]:
        """Get the keys of the logged data hooks

        Returns
        -------
        set[str]
            The set of hook names for which data was logged.

        """
        return set(self._hooked_model_inference_results.keys())

    def __len__(self) -> int:
        """Get the number of samples for which data was logged.

        Returns
        -------
        int
            The number of samples for which data was logged.
        """

        return next(iter(self._hooked_model_inference_results.values())).shape[0]
