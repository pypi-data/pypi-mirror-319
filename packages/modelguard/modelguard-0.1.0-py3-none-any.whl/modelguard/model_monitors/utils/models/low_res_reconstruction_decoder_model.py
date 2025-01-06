import torch
from torch.nn import BatchNorm2d, Conv2d, LazyLinear, Module, ReLU, Sequential, Upsample


class UpsampleBlock(Module):
    """Upsample block architecture for upsampling tensors."""

    def __init__(self, scale_factor: int, in_channels: int, out_channels: int):
        """Initialize the UpsampleBlock.

        Parameters
        ----------
        scale_factor
            The factor for how much to upsample the input tensor. Note that this will
            only upsample along the height and width dimensions of the tensor.
        in_channels
            The number of channels of the original input tensor.
        out_channels
            The required number of channels for the final output tensor.

        """
        super().__init__()  # type: ignore

        self.upsample = Upsample(scale_factor=scale_factor)

        self.double_conv = Sequential(
            Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            BatchNorm2d(out_channels),
            ReLU(inplace=True),
            Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            BatchNorm2d(out_channels),
            ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Run inference on the UpsampleBlock.

        Parameters
        ----------
        x
            The input.

        Returns
        -------
        Tensor
            The upsampled input.


        """
        x = self.upsample(x)
        return self.double_conv(x)


class LowResReconstructionDecoderModel(Module):
    """Decoder model architecture for generating low-resolution tensors
    from an input vector.

    The tensors that are generated have a shape of (N, out_channels, 16, 16), with N
    being the batch dimension and the number of output channels being a hyperparameter
    of the model.

    """

    def __init__(self, out_channels: int):
        """Initialize the LowResReconstructionDecoderModel model instance.

        Parameters
        ----------
        out_channels
            The required number of channels for the final output tensor.

        """
        super().__init__()  # type: ignore

        # Lazy linear because we don't know the dim of the input latent vector
        self.in_linear = LazyLinear(1024)

        self.up1 = UpsampleBlock(2, 64, 32)  # out: (32, 8, 8)
        self.up2 = UpsampleBlock(2, 32, 16)  # out: (16, 16, 16)

        self.out_conv = Conv2d(16, out_channels, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Use the LowResReconstructionDecoderModel model instance for inference.

        Parameters
        ----------
        x
            The input.

        Returns
        -------
        Tensor
            The generated low-resolution tensor. The shape is (N, out_channels, 16, 16)
            with `N` being the batch dimension.

        """

        # The first layer should flatten the input latent vector in case it has multiple
        # dimensions
        x = torch.flatten(x, start_dim=1)

        x = self.in_linear(x)

        # Reshape to build the original tensor from which to start upsampling
        x = torch.reshape(x, (-1, 64, 4, 4))

        # Pass through the network
        x = self.up1(x)
        x = self.up2(x)
        return self.out_conv(x)
