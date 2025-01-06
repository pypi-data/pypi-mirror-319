import torch
from torch.nn import Module

from modelguard.config import Config


def run_torch_model_inference(model: Module, x: torch.Tensor) -> torch.Tensor:
    """Run inference of a torch model on a batch of samples.

    Parameters
    ----------
    x
        The batch of samples to run inference on. The first dimension of this sample
        tensor should be the batch dimension.

    Returns
    -------
    Tensor
        The model output (already detached and moved to CPU device)

    """

    with torch.no_grad():
        # Move the model and input to the inference device
        model.to(Config.DEVICE)
        x = x.to(Config.DEVICE)

        # Run inference on the model
        model_out = model(x)

        # Move the model back to cpu
        model.cpu()

    return model_out.detach().cpu()
