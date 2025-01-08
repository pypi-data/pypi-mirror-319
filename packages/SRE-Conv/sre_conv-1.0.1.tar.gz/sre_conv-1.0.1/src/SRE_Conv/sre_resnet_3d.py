from functools import partial
from typing import Any, Callable, List, Optional, Sequence, Tuple, Type, Union

import torch.nn as nn
from torch import Tensor

from torchvision.transforms._presets import VideoClassification
from torchvision.utils import _log_api_usage_once
from torchvision.models._api import Weights, WeightsEnum
from torchvision.models._meta import _KINETICS400_CATEGORIES
from torchvision.models._utils import _ovewrite_named_param, handle_legacy_interface

from .sre_conv import SRE_Conv2d, SRE_Conv3d
from .sre_resnet import _repeat

__all__ = [
    "VideoResNet",
    "R3D_18_Weights",
    "MC3_18_Weights",
    "R2Plus1D_18_Weights",
    "r3d_18",
    "mc3_18",
    "r2plus1d_18",
]


class Conv3DSimple(nn.Conv3d):
    def __init__(
        self,
        in_planes: int,
        out_planes: int,
        midplanes: Optional[int] = None,
        stride: int = 1,
        padding: int = 1,
    ) -> None:

        super().__init__(
            in_channels=in_planes,
            out_channels=out_planes,
            kernel_size=(3, 3, 3),
            stride=stride,
            padding=padding,
            bias=False,
        )

    @staticmethod
    def get_downsample_stride(stride: int) -> Tuple[int, int, int]:
        return stride, stride, stride


class SREConv3D(SRE_Conv3d):
    def __init__(
        self,
        in_planes: int,
        out_planes: int,
        midplanes: Optional[int] = None,
        stride: int = 1,
        padding: int = 1,
        kernel_size: int = 3,
        sre_k: int = None,
    ) -> None:

        super().__init__(
            in_channels=in_planes,
            out_channels=out_planes,
            kernel_size=(kernel_size, kernel_size, kernel_size),
            stride=stride,
            padding=kernel_size // 2,
            sre_k=sre_k,
            bias=False,
        )

    @staticmethod
    def get_downsample_stride(stride: int) -> Tuple[int, int, int]:
        return stride, stride, stride


class Conv2Plus1D(nn.Sequential):
    def __init__(
        self,
        in_planes: int,
        out_planes: int,
        midplanes: int,
        stride: int = 1,
        padding: int = 1,
    ) -> None:
        super().__init__(
            nn.Conv3d(
                in_planes,
                midplanes,
                kernel_size=(1, 3, 3),
                stride=(1, stride, stride),
                padding=(0, padding, padding),
                bias=False,
            ),
            nn.BatchNorm3d(midplanes),
            nn.ReLU(inplace=True),
            nn.Conv3d(
                midplanes,
                out_planes,
                kernel_size=(3, 1, 1),
                stride=(stride, 1, 1),
                padding=(padding, 0, 0),
                bias=False,
            ),
        )

    @staticmethod
    def get_downsample_stride(stride: int) -> Tuple[int, int, int]:
        return stride, stride, stride


class Conv3DNoTemporal(nn.Conv3d):
    def __init__(
        self,
        in_planes: int,
        out_planes: int,
        midplanes: Optional[int] = None,
        stride: int = 1,
        padding: int = 1,
    ) -> None:

        super().__init__(
            in_channels=in_planes,
            out_channels=out_planes,
            kernel_size=(1, 3, 3),
            stride=(1, stride, stride),
            padding=(0, padding, padding),
            bias=False,
        )

    @staticmethod
    def get_downsample_stride(stride: int) -> Tuple[int, int, int]:
        return 1, stride, stride


class SREBasicBlock(nn.Module):

    expansion = 1

    def __init__(
        self,
        inplanes: int,
        planes: int,
        conv_builder: Callable[..., nn.Module],
        stride: int = 1,
        downsample: Optional[nn.Module] = None,
        sre_size: int = 3,
        sre_k: int = None,
    ) -> None:
        midplanes = (inplanes * planes * 3 * 3 * 3) // (inplanes * 3 * 3 + 3 * planes)

        super().__init__()
        if stride > 1:
            down_pooling = nn.AvgPool3d(
                kernel_size=(stride, stride, stride), stride=(stride, stride, stride)
            )
        else:
            down_pooling = nn.Identity()
        self.conv1 = nn.Sequential(
            down_pooling,
            conv_builder(
                inplanes, planes, midplanes, 1, kernel_size=sre_size, sre_k=sre_k
            ),
            nn.BatchNorm3d(planes),
            nn.ReLU(inplace=True),
        )
        self.conv2 = nn.Sequential(
            conv_builder(planes, planes, midplanes, kernel_size=sre_size, sre_k=sre_k),
            nn.BatchNorm3d(planes),
        )
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x: Tensor) -> Tensor:
        residual = x

        out = self.conv1(x)
        out = self.conv2(out)
        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


class BasicBlock(nn.Module):

    expansion = 1

    def __init__(
        self,
        inplanes: int,
        planes: int,
        conv_builder: Callable[..., nn.Module],
        stride: int = 1,
        downsample: Optional[nn.Module] = None,
        **kwargs,
    ) -> None:
        midplanes = (inplanes * planes * 3 * 3 * 3) // (inplanes * 3 * 3 + 3 * planes)

        super().__init__()
        self.conv1 = nn.Sequential(
            conv_builder(inplanes, planes, midplanes, stride),
            nn.BatchNorm3d(planes),
            nn.ReLU(inplace=True),
        )
        self.conv2 = nn.Sequential(
            conv_builder(planes, planes, midplanes), nn.BatchNorm3d(planes)
        )
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x: Tensor) -> Tensor:
        residual = x

        out = self.conv1(x)
        out = self.conv2(out)
        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


class Bottleneck(nn.Module):
    expansion = 4

    def __init__(
        self,
        inplanes: int,
        planes: int,
        conv_builder: Callable[..., nn.Module],
        stride: int = 1,
        downsample: Optional[nn.Module] = None,
        **kwargs,
    ) -> None:

        super().__init__()
        midplanes = (inplanes * planes * 3 * 3 * 3) // (inplanes * 3 * 3 + 3 * planes)

        # 1x1x1
        self.conv1 = nn.Sequential(
            nn.Conv3d(inplanes, planes, kernel_size=1, bias=False),
            nn.BatchNorm3d(planes),
            nn.ReLU(inplace=True),
        )
        # Second kernel
        self.conv2 = nn.Sequential(
            conv_builder(planes, planes, midplanes, stride),
            nn.BatchNorm3d(planes),
            nn.ReLU(inplace=True),
        )

        # 1x1x1
        self.conv3 = nn.Sequential(
            nn.Conv3d(planes, planes * self.expansion, kernel_size=1, bias=False),
            nn.BatchNorm3d(planes * self.expansion),
        )
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x: Tensor) -> Tensor:
        residual = x

        out = self.conv1(x)
        out = self.conv2(out)
        out = self.conv3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


class BasicStem(nn.Sequential):
    """The default conv-batchnorm-relu stem"""

    def __init__(self, in_channels=3) -> None:
        super().__init__(
            nn.Conv3d(
                in_channels,
                64,
                kernel_size=(3, 7, 7),
                stride=(1, 1, 1),
                padding=(1, 3, 3),
                bias=False,
            ),
            nn.BatchNorm3d(64),
            nn.ReLU(inplace=True),
        )


class SREBasicStem(nn.Sequential):
    """The default conv-batchnorm-relu stem"""

    def __init__(self, in_channels=3) -> None:
        super().__init__(
            SRE_Conv3d(
                in_channels,
                64,
                kernel_size=(3, 7, 7),
                stride=(1, 1, 1),
                padding=(1, 3, 3),
                bias=False,
            ),
            nn.BatchNorm3d(64),
            nn.ReLU(inplace=True),
        )


class R2Plus1dStem(nn.Sequential):
    """R(2+1)D stem is different than the default one as it uses separated 3D convolution"""

    def __init__(self, in_channels=3) -> None:
        super().__init__(
            nn.Conv3d(
                in_channels,
                45,
                kernel_size=(1, 7, 7),
                stride=(1, 2, 2),
                padding=(0, 3, 3),
                bias=False,
            ),
            nn.BatchNorm3d(45),
            nn.ReLU(inplace=True),
            nn.Conv3d(
                45,
                64,
                kernel_size=(3, 1, 1),
                stride=(1, 1, 1),
                padding=(1, 0, 0),
                bias=False,
            ),
            nn.BatchNorm3d(64),
            nn.ReLU(inplace=True),
        )


class VideoResNet(nn.Module):
    def __init__(
        self,
        block: Type[Union[BasicBlock, SREBasicBlock, Bottleneck]],
        conv_makers: Sequence[
            Type[Union[Conv3DSimple, SREConv3D, Conv3DNoTemporal, Conv2Plus1D]]
        ],
        layers: List[int],
        stem: Callable[..., nn.Module],
        num_classes: int = 400,
        zero_init_residual: bool = False,
        in_channels: int = 3,
        sre_conv_size: Union[int, list] = 3,
        sre_k: Union[int, list] = None,
    ) -> None:
        """Generic resnet video generator.

        Args:
            block (Type[Union[BasicBlock, Bottleneck]]): resnet building block
            conv_makers (List[Type[Union[Conv3DSimple, Conv3DNoTemporal, Conv2Plus1D]]]): generator
                function for each layer
            layers (List[int]): number of blocks per layer
            stem (Callable[..., nn.Module]): module specifying the ResNet stem.
            num_classes (int, optional): Dimension of the final FC layer. Defaults to 400.
            zero_init_residual (bool, optional): Zero init bottleneck residual BN. Defaults to False.
        """
        super().__init__()
        self.inplanes = 64
        self.sre_conv_size = _repeat(sre_conv_size, 4)
        self.sre_k = _repeat(sre_k, 4)

        self.stem = stem(in_channels=in_channels)

        self.layer1 = self._make_layer(
            block,
            conv_makers[0],
            64,
            layers[0],
            stride=1,
            sre_conv_size=self.sre_conv_size[0],
            sre_k=self.sre_k[0],
        )
        self.layer2 = self._make_layer(
            block,
            conv_makers[1],
            128,
            layers[1],
            stride=2,
            sre_conv_size=self.sre_conv_size[1],
            sre_k=self.sre_k[1],
        )
        self.layer3 = self._make_layer(
            block,
            conv_makers[2],
            256,
            layers[2],
            stride=2,
            sre_conv_size=self.sre_conv_size[2],
            sre_k=self.sre_k[2],
        )
        self.layer4 = self._make_layer(
            block,
            conv_makers[3],
            512,
            layers[3],
            stride=2,
            sre_conv_size=self.sre_conv_size[3],
            sre_k=self.sre_k[3],
        )

        self.avgpool = nn.AdaptiveAvgPool3d((1, 1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

        # init weights
        for m in self.modules():
            if isinstance(m, nn.Conv3d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm3d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

        if zero_init_residual:
            for m in self.modules():
                if isinstance(m, Bottleneck):
                    nn.init.constant_(m.bn3.weight, 0)  # type: ignore[union-attr, arg-type]

    def forward(self, x: Tensor) -> Tensor:
        x = self.stem(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        # Flatten the layer to fc
        x = x.flatten(1)
        x = self.fc(x)

        return x

    def _make_layer(
        self,
        block: Type[Union[BasicBlock, SREBasicBlock, Bottleneck]],
        conv_builder: Type[
            Union[Conv3DSimple, SREConv3D, Conv3DNoTemporal, Conv2Plus1D]
        ],
        planes: int,
        blocks: int,
        stride: int = 1,
        sre_conv_size: int = 3,
        sre_k: int = None,
    ) -> nn.Sequential:
        downsample = None

        if stride != 1 or self.inplanes != planes * block.expansion:
            ds_stride = conv_builder.get_downsample_stride(stride)
            if conv_builder == SREConv3D:
                downsample = nn.Sequential(
                    nn.AvgPool3d(kernel_size=ds_stride, stride=ds_stride),
                    nn.Conv3d(
                        self.inplanes,
                        planes * block.expansion,
                        kernel_size=1,
                        stride=1,
                        bias=False,
                    ),
                    nn.BatchNorm3d(planes * block.expansion),
                )
            else:
                downsample = nn.Sequential(
                    nn.Conv3d(
                        self.inplanes,
                        planes * block.expansion,
                        kernel_size=1,
                        stride=ds_stride,
                        bias=False,
                    ),
                    nn.BatchNorm3d(planes * block.expansion),
                )
        layers = []
        layers.append(
            block(
                self.inplanes,
                planes,
                conv_builder,
                stride,
                downsample,
                sre_size=sre_conv_size,
            )
        )

        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(
                block(self.inplanes, planes, conv_builder, sre_size=sre_conv_size)
            )

        return nn.Sequential(*layers)


def _video_resnet(
    block: Type[Union[BasicBlock, Bottleneck]],
    conv_makers: Sequence[Type[Union[Conv3DSimple, Conv3DNoTemporal, Conv2Plus1D]]],
    layers: List[int],
    stem: Callable[..., nn.Module],
    weights: Optional[WeightsEnum],
    progress: bool,
    **kwargs: Any,
) -> VideoResNet:
    if weights is not None:
        _ovewrite_named_param(kwargs, "num_classes", len(weights.meta["categories"]))

    model = VideoResNet(block, conv_makers, layers, stem, **kwargs)

    if weights is not None:
        model.load_state_dict(weights.get_state_dict(progress=progress))

    return model


_COMMON_META = {
    "min_size": (1, 1),
    "categories": _KINETICS400_CATEGORIES,
    "recipe": "https://github.com/pytorch/vision/tree/main/references/video_classification",
    "_docs": (
        "The weights reproduce closely the accuracy of the paper. The accuracies are estimated on video-level "
        "with parameters `frame_rate=15`, `clips_per_video=5`, and `clip_len=16`."
    ),
}


class R3D_18_Weights(WeightsEnum):
    KINETICS400_V1 = Weights(
        url="https://download.pytorch.org/models/r3d_18-b3b3357e.pth",
        transforms=partial(
            VideoClassification, crop_size=(112, 112), resize_size=(128, 171)
        ),
        meta={
            **_COMMON_META,
            "num_params": 33371472,
            "_metrics": {
                "Kinetics-400": {
                    "acc@1": 63.200,
                    "acc@5": 83.479,
                }
            },
        },
    )
    DEFAULT = KINETICS400_V1


class MC3_18_Weights(WeightsEnum):
    KINETICS400_V1 = Weights(
        url="https://download.pytorch.org/models/mc3_18-a90a0ba3.pth",
        transforms=partial(
            VideoClassification, crop_size=(112, 112), resize_size=(128, 171)
        ),
        meta={
            **_COMMON_META,
            "num_params": 11695440,
            "_metrics": {
                "Kinetics-400": {
                    "acc@1": 63.960,
                    "acc@5": 84.130,
                }
            },
        },
    )
    DEFAULT = KINETICS400_V1


class R2Plus1D_18_Weights(WeightsEnum):
    KINETICS400_V1 = Weights(
        url="https://download.pytorch.org/models/r2plus1d_18-91a641e6.pth",
        transforms=partial(
            VideoClassification, crop_size=(112, 112), resize_size=(128, 171)
        ),
        meta={
            **_COMMON_META,
            "num_params": 31505325,
            "_metrics": {
                "Kinetics-400": {
                    "acc@1": 67.463,
                    "acc@5": 86.175,
                }
            },
        },
    )
    DEFAULT = KINETICS400_V1


@handle_legacy_interface(weights=("pretrained", R3D_18_Weights.KINETICS400_V1))
def r3d_18(
    *, weights: Optional[R3D_18_Weights] = None, progress: bool = True, **kwargs: Any
) -> VideoResNet:
    """Construct 18 layer Resnet3D model.

    .. betastatus:: video module

    Reference: `A Closer Look at Spatiotemporal Convolutions for Action Recognition <https://arxiv.org/abs/1711.11248>`__.

    Args:
        weights (:class:`~torchvision.models.video.R3D_18_Weights`, optional): The
            pretrained weights to use. See
            :class:`~torchvision.models.video.R3D_18_Weights`
            below for more details, and possible values. By default, no
            pre-trained weights are used.
        progress (bool): If True, displays a progress bar of the download to stderr. Default is True.
        **kwargs: parameters passed to the ``torchvision.models.video.resnet.VideoResNet`` base class.
            Please refer to the `source code
            <https://github.com/pytorch/vision/blob/main/torchvision/models/video/resnet.py>`_
            for more details about this class.

    .. autoclass:: torchvision.models.video.R3D_18_Weights
        :members:
    """
    weights = R3D_18_Weights.verify(weights)

    return _video_resnet(
        BasicBlock,
        [Conv3DSimple] * 4,
        [2, 2, 2, 2],
        BasicStem,
        weights,
        progress,
        **kwargs,
    )


def sre_r3d_18(*, progress: bool = True, **kwargs: Any) -> VideoResNet:
    """Construct SRE 18 layer Resnet3D model.

    .. betastatus:: video module

    .. autoclass:: torchvision.models.video.R3D_18_Weights
        :members:
    """
    return _video_resnet(
        SREBasicBlock,
        [SREConv3D] * 4,
        [2, 2, 2, 2],
        SREBasicStem,
        None,
        progress,
        **kwargs,
    )


@handle_legacy_interface(weights=("pretrained", MC3_18_Weights.KINETICS400_V1))
def mc3_18(
    *, weights: Optional[MC3_18_Weights] = None, progress: bool = True, **kwargs: Any
) -> VideoResNet:
    """Construct 18 layer Mixed Convolution network as in

    .. betastatus:: video module

    Reference: `A Closer Look at Spatiotemporal Convolutions for Action Recognition <https://arxiv.org/abs/1711.11248>`__.

    Args:
        weights (:class:`~torchvision.models.video.MC3_18_Weights`, optional): The
            pretrained weights to use. See
            :class:`~torchvision.models.video.MC3_18_Weights`
            below for more details, and possible values. By default, no
            pre-trained weights are used.
        progress (bool): If True, displays a progress bar of the download to stderr. Default is True.
        **kwargs: parameters passed to the ``torchvision.models.video.resnet.VideoResNet`` base class.
            Please refer to the `source code
            <https://github.com/pytorch/vision/blob/main/torchvision/models/video/resnet.py>`_
            for more details about this class.

    .. autoclass:: torchvision.models.video.MC3_18_Weights
        :members:
    """
    weights = MC3_18_Weights.verify(weights)

    return _video_resnet(
        BasicBlock,
        [Conv3DSimple] + [Conv3DNoTemporal] * 3,  # type: ignore[list-item]
        [2, 2, 2, 2],
        BasicStem,
        weights,
        progress,
        **kwargs,
    )


@handle_legacy_interface(weights=("pretrained", R2Plus1D_18_Weights.KINETICS400_V1))
def r2plus1d_18(
    *,
    weights: Optional[R2Plus1D_18_Weights] = None,
    progress: bool = True,
    **kwargs: Any,
) -> VideoResNet:
    """Construct 18 layer deep R(2+1)D network as in

    .. betastatus:: video module

    Reference: `A Closer Look at Spatiotemporal Convolutions for Action Recognition <https://arxiv.org/abs/1711.11248>`__.

    Args:
        weights (:class:`~torchvision.models.video.R2Plus1D_18_Weights`, optional): The
            pretrained weights to use. See
            :class:`~torchvision.models.video.R2Plus1D_18_Weights`
            below for more details, and possible values. By default, no
            pre-trained weights are used.
        progress (bool): If True, displays a progress bar of the download to stderr. Default is True.
        **kwargs: parameters passed to the ``torchvision.models.video.resnet.VideoResNet`` base class.
            Please refer to the `source code
            <https://github.com/pytorch/vision/blob/main/torchvision/models/video/resnet.py>`_
            for more details about this class.

    .. autoclass:: torchvision.models.video.R2Plus1D_18_Weights
        :members:
    """
    weights = R2Plus1D_18_Weights.verify(weights)

    return _video_resnet(
        BasicBlock,
        [Conv2Plus1D] * 4,
        [2, 2, 2, 2],
        R2Plus1dStem,
        weights,
        progress,
        **kwargs,
    )


# The dictionary below is internal implementation detail and will be removed in v0.15
from torchvision.models._utils import _ModelURLs


model_urls = _ModelURLs(
    {
        "r3d_18": R3D_18_Weights.KINETICS400_V1.url,
        "mc3_18": MC3_18_Weights.KINETICS400_V1.url,
        "r2plus1d_18": R2Plus1D_18_Weights.KINETICS400_V1.url,
    }
)
