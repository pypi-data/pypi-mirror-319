import torch
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """The ModelGuard project configurations.

    Attributes
    ----------
    SEED
        The random seed to use throughout the package.
    DEVICE
        The torch device to use when training or running inference of a model. This
        will be set to CUDA if available, otherwise the CPU will be used.
    DATALOADER_NUM_WORKERS
        The number of workers to use for the torch DataLoaders in model monitoring
        techniques that have an underlying torch model that needs to be trained.
    """

    SEED: int = 0

    # Hardware parameters
    DEVICE: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    DATALOADER_NUM_WORKERS: int = 4
