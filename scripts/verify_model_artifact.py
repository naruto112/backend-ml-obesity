"""Verify the ML model artifact against its manifest."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from repo root without install.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ml.model_loader import ModelArtifactError, verify_artifact  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/verify_model_artifact.py <manifest_path> [model_path]")
        sys.exit(1)

    manifest_path = Path(sys.argv[1])
    if len(sys.argv) >= 3:
        model_path = Path(sys.argv[2])
    else:
        model_path = manifest_path.parent / "hgb.joblib"

    try:
        manifest = verify_artifact(model_path, manifest_path)
        print(f"Model:     {manifest.get('name')} v{manifest.get('version')}")
        print(f"Algorithm: {manifest.get('algorithm')}")
        print(f"SHA-256:   {manifest.get('sha256')}")
        print(f"Size:      {manifest.get('size_bytes')} bytes")
        print(f"Features:  {len(manifest.get('features', []))}")
        print(f"Classes:   {len(manifest.get('class_map', {}))}")
        print("Verification: PASSED")
    except ModelArtifactError as e:
        print(f"Verification: FAILED - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
