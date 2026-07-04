"""Load and verify the ML model artifact."""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

import joblib  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


class ModelArtifactError(RuntimeError):
    """The model artifact failed integrity or compatibility checks."""


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_artifact(model_path: Path, manifest_path: Path) -> dict[str, Any]:
    """Verify the artifact against its manifest. Returns the manifest dict."""
    if not manifest_path.exists():
        raise ModelArtifactError(f"Manifest not found: {manifest_path}")
    if not model_path.exists():
        raise ModelArtifactError(f"Model file not found: {model_path}")

    with open(manifest_path) as f:
        manifest: dict[str, Any] = json.load(f)

    expected_sha = str(manifest["sha256"])
    actual_sha = _sha256(model_path)
    if actual_sha != expected_sha:
        raise ModelArtifactError(f"SHA-256 mismatch: expected {expected_sha}, got {actual_sha}")

    expected_size = int(manifest["size_bytes"])
    actual_size = model_path.stat().st_size
    if actual_size != expected_size:
        raise ModelArtifactError(f"Size mismatch: expected {expected_size}, got {actual_size}")

    return manifest


def load_model(model_path: Path, manifest_path: Path) -> Any:
    """Verify and load the model artifact. Raises ModelArtifactError on failure."""
    manifest = verify_artifact(model_path, manifest_path)

    model = joblib.load(model_path)

    model_type = type(model).__name__
    expected_algorithm = str(manifest.get("algorithm", ""))
    if expected_algorithm and model_type != expected_algorithm:
        raise ModelArtifactError(
            f"Model type mismatch: expected {expected_algorithm}, got {model_type}"
        )

    expected_features = list(manifest.get("features", []))
    if hasattr(model, "feature_names_in_"):
        actual_features = list(model.feature_names_in_)
        if actual_features != expected_features:
            raise ModelArtifactError(
                f"Feature mismatch: expected {expected_features}, got {actual_features}"
            )

    logger.info(
        "model_loaded",
        extra={
            "model_name": manifest.get("name"),
            "model_version": manifest.get("version"),
            "sha256_short": str(manifest["sha256"])[:12],
        },
    )

    return model
