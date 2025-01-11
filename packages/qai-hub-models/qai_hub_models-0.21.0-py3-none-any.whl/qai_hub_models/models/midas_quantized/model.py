# ---------------------------------------------------------------------
# Copyright (c) 2024 Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# ---------------------------------------------------------------------
from __future__ import annotations

# isort: off
# This verifies aimet is installed, and this must be included first.
from qai_hub_models.utils.quantization_aimet import (
    AIMETQuantizableMixin,
    constrain_quantized_inputs_to_image_range,
    tie_observers,
    convert_all_depthwise_to_per_tensor,
)

# isort: on

import torch
from aimet_torch.batch_norm_fold import fold_all_batch_norms
from aimet_torch.cross_layer_equalization import CrossLayerScaling
from aimet_torch.model_preparer import prepare_model
from aimet_torch.quantsim import QuantizationSimModel

from qai_hub_models.models.midas.model import Midas
from qai_hub_models.utils.aimet.config_loader import get_default_aimet_config
from qai_hub_models.utils.asset_loaders import CachedWebModelAsset

MODEL_ID = __name__.split(".")[-2]
MODEL_ASSET_VERSION = 1
DEFAULT_ENCODINGS = "midas_quantized_encodings.json"


class MidasQuantizable(AIMETQuantizableMixin, Midas):
    """Midas with post train quantization support.

    Supports only 8 bit weights and activations, and only loads pre-quantized checkpoints.
    Support for quantizing using your own weights & data will come at a later date."""

    def __init__(
        self,
        model: QuantizationSimModel,
    ) -> None:
        # Input is already normalized by sim_model. Disable it in the wrapper model.
        Midas.__init__(self, model.model, normalize_input=False)
        AIMETQuantizableMixin.__init__(
            self,
            model,
        )

    @classmethod
    def from_pretrained(
        cls,
        aimet_encodings: str | None = "DEFAULT",
    ) -> MidasQuantizable:
        """
        Parameters:
          aimet_encodings:
            if "DEFAULT": Loads the model with aimet encodings calibrated on imagenette.
            elif None: Doesn't load any encodings. Used when computing encodings.
            else: Interprets as a filepath and loads the encodings stored there.
        """
        model = Midas.from_pretrained()
        input_shape = cls.get_input_spec()["image"][0]
        dummy_input = torch.rand(input_shape)

        model = prepare_model(model)
        fold_all_batch_norms(model, input_shape, dummy_input)
        CrossLayerScaling.scale_model(model, input_shape, dummy_input)
        sim = QuantizationSimModel(
            model,
            quant_scheme="tf_enhanced",
            default_param_bw=8,
            default_output_bw=8,
            config_file=get_default_aimet_config(),
            dummy_input=dummy_input,
        )
        convert_all_depthwise_to_per_tensor(sim.model)
        tie_observers(sim)
        constrain_quantized_inputs_to_image_range(sim)

        if aimet_encodings:
            if aimet_encodings == "DEFAULT":
                aimet_encodings = CachedWebModelAsset.from_asset_store(
                    MODEL_ID, MODEL_ASSET_VERSION, DEFAULT_ENCODINGS
                ).fetch()
            sim.load_encodings(aimet_encodings, strict=False)

        return cls(sim)

    def forward(self, image):
        """
        Runs the model on an image tensor and returns a tensor of depth estimates

        Parameters:
            image: A [1, 3, H, W] image.
                   Pixel values pre-processed for encoder consumption.
                   Range: float[0, 1] if self.normalize_input, else ~[-2.5, 2.5]
                   3-channel Color Space: RGB

        Returns:
            Tensor of depth estimates of size [1, H, W].
        """
        return self.model(image)
