"""Generate a model manifest from a serialized artifact.

Reads the .joblib model, extracts what can be derived automatically (SHA-256,
size, algorithm, features, scikit-learn version, class codes) and reuses the
metadata that cannot be inferred (name, version, class_map labels, provenance)
from the existing manifest when present. The output is meant to be reviewed and
edited by hand before committing.

Usage:
    python scripts/generate_model_manifest.py <model_path> [manifest_out]

    # Print to stdout instead of writing:
    python scripts/generate_model_manifest.py artifacts/hgb.joblib -

Examples:
    python scripts/generate_model_manifest.py artifacts/hgb.joblib
    python scripts/generate_model_manifest.py artifacts/hgb.joblib artifacts/hgb.manifest.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import joblib  # type: ignore[import-untyped]

# Allow running from repo root without install.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _sklearn_version() -> str:
    try:
        import sklearn  # type: ignore[import-untyped]

        return str(sklearn.__version__)
    except ImportError:
        return ""


def build_manifest(model_path: Path, previous: dict[str, Any]) -> dict[str, Any]:
    """Build a manifest dict for ``model_path``, reusing ``previous`` metadata."""
    model = joblib.load(model_path)

    features = list(getattr(model, "feature_names_in_", []))
    classes = [int(c) for c in getattr(model, "classes_", [])]

    # class_map labels cannot be inferred from the model. Reuse the previous
    # mapping where the code still exists, otherwise leave a placeholder to edit.
    previous_class_map = {str(k): v for k, v in previous.get("class_map", {}).items()}
    class_map = {str(code): previous_class_map.get(str(code), "TODO") for code in classes}

    return {
        "name": previous.get("name", model_path.stem),
        "version": previous.get("version", "0.0.0"),
        "algorithm": type(model).__name__,
        "scikit_learn_version": _sklearn_version(),
        "sha256": _sha256(model_path),
        "size_bytes": model_path.stat().st_size,
        "features": features,
        "class_map": class_map,
        "provenance": previous.get("provenance", {}),
    }


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(
            "Usage: python scripts/generate_model_manifest.py <model_path> [manifest_out|-]",
            file=sys.stderr,
        )
        sys.exit(1)

    model_path = Path(args[0])
    if not model_path.exists():
        print(f"Model file not found: {model_path}", file=sys.stderr)
        sys.exit(1)

    if len(args) >= 2:
        out_arg = args[1]
    else:
        out_arg = str(model_path.with_suffix(".manifest.json"))

    manifest_path = None if out_arg == "-" else Path(out_arg)

    previous: dict[str, Any] = {}
    if manifest_path is not None and manifest_path.exists():
        with open(manifest_path) as f:
            previous = json.load(f)

    manifest = build_manifest(model_path, previous)
    rendered = json.dumps(manifest, indent=2, ensure_ascii=False)

    if manifest_path is None:
        print(rendered)
    else:
        manifest_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Manifest written to {manifest_path}", file=sys.stderr)
        print("Review and edit the fields marked 'TODO' before committing.", file=sys.stderr)


if __name__ == "__main__":
    main()
