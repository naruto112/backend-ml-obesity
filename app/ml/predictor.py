"""Predict the obesity class from the 12 API input fields."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import numpy as np

from app.domain_catalog import OBESITY_CLASSES
from app.ml.feature_transformer import FeatureTransformer

CLASS_MAP: dict[int, str] = dict(enumerate(OBESITY_CLASSES))


class PredictionError(RuntimeError):
    """The model returned an unexpected prediction."""


class ObesityPredictor:
    """Combine feature transformation and model inference."""

    def __init__(self, model: Any, transformer: FeatureTransformer | None = None) -> None:
        self._model = model
        self._transformer = transformer or FeatureTransformer()

    def predict(self, command: Mapping[str, Any]) -> str:
        features = self._transformer.transform(command)
        raw = self._model.predict(features)

        if raw is None or (hasattr(raw, "__len__") and len(raw) != 1):
            raise PredictionError("Model returned unexpected output shape")

        code = int(raw[0]) if not isinstance(raw[0], (int, np.integer)) else int(raw[0])

        label = CLASS_MAP.get(code)
        if label is None:
            raise PredictionError(f"Unknown prediction code: {code}")

        return label
