"""Tests for app.ml package (feature_transformer, model_loader, predictor)."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from app.ml.feature_transformer import FEATURE_COLUMNS, FeatureTransformer
from app.ml.model_loader import ModelArtifactError, _sha256, load_model, verify_artifact
from app.ml.predictor import CLASS_MAP, ObesityPredictor, PredictionError

SAMPLE_COMMAND = {
    "idade": 25,
    "sexo_biologico": 1,
    "come_vegetaiis": 2,
    "refeicoes_diariamente": 3,
    "come_entre_refeicao": "somentimes",
    "litro_agua": 2,
    "frequencia_semanal_atvidade_fisica": 1,
    "horas_dispositivo_eletronico": 1,
    "consome_bebida_alcoolica": "no",
    "historico_familiar": "yes",
    "alimentos_calorico": "no",
    "monitora_calorias": "no",
    "fuma": "no",
    "meio_transporte": "public_transportation",
}


class TestFeatureTransformer:
    def test_output_shape_and_columns(self):
        transformer = FeatureTransformer()
        df = transformer.transform(SAMPLE_COMMAND)
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == FEATURE_COLUMNS
        assert len(df) == 1

    def test_ordinal_mapping(self):
        transformer = FeatureTransformer()
        df = transformer.transform(SAMPLE_COMMAND)
        assert df["CAEC"].iloc[0] == 1  # somentimes
        assert df["CALC"].iloc[0] == 0  # no

    def test_gender_encoding(self):
        transformer = FeatureTransformer()
        male_cmd = {**SAMPLE_COMMAND, "sexo_biologico": 1}
        female_cmd = {**SAMPLE_COMMAND, "sexo_biologico": 2}
        assert transformer.transform(male_cmd)["Gender_Male"].iloc[0] == 1
        assert transformer.transform(female_cmd)["Gender_Male"].iloc[0] == 0

    def test_family_history_encoding(self):
        transformer = FeatureTransformer()
        yes_cmd = {**SAMPLE_COMMAND, "historico_familiar": "yes"}
        no_cmd = {**SAMPLE_COMMAND, "historico_familiar": "no"}
        assert transformer.transform(yes_cmd)["family_history_yes"].iloc[0] == 1
        assert transformer.transform(no_cmd)["family_history_yes"].iloc[0] == 0

    def test_favc_encoding(self):
        transformer = FeatureTransformer()
        yes_cmd = {**SAMPLE_COMMAND, "alimentos_calorico": "yes"}
        no_cmd = {**SAMPLE_COMMAND, "alimentos_calorico": "no"}
        assert transformer.transform(yes_cmd)["FAVC_yes"].iloc[0] == 1
        assert transformer.transform(no_cmd)["FAVC_yes"].iloc[0] == 0

    def test_scc_encoding(self):
        transformer = FeatureTransformer()
        yes_cmd = {**SAMPLE_COMMAND, "monitora_calorias": "yes"}
        no_cmd = {**SAMPLE_COMMAND, "monitora_calorias": "no"}
        assert transformer.transform(yes_cmd)["SCC_yes"].iloc[0] == 1
        assert transformer.transform(no_cmd)["SCC_yes"].iloc[0] == 0

    def test_smoke_encoding(self):
        transformer = FeatureTransformer()
        yes_cmd = {**SAMPLE_COMMAND, "fuma": "yes"}
        no_cmd = {**SAMPLE_COMMAND, "fuma": "no"}
        assert transformer.transform(yes_cmd)["SMOKE_yes"].iloc[0] == 1
        assert transformer.transform(no_cmd)["SMOKE_yes"].iloc[0] == 0

    def test_mtrans_encoding_public_transportation(self):
        transformer = FeatureTransformer()
        df = transformer.transform(SAMPLE_COMMAND)
        assert df["MTRANS_Bike"].iloc[0] == 0
        assert df["MTRANS_Motorbike"].iloc[0] == 0
        assert df["MTRANS_Public_Transportation"].iloc[0] == 1
        assert df["MTRANS_Walking"].iloc[0] == 0

    def test_mtrans_automobile_produces_all_zeros(self):
        transformer = FeatureTransformer()
        cmd = {**SAMPLE_COMMAND, "meio_transporte": "automobile"}
        df = transformer.transform(cmd)
        assert df["MTRANS_Bike"].iloc[0] == 0
        assert df["MTRANS_Motorbike"].iloc[0] == 0
        assert df["MTRANS_Public_Transportation"].iloc[0] == 0
        assert df["MTRANS_Walking"].iloc[0] == 0


class TestModelLoader:
    def test_verify_artifact_missing_manifest(self, tmp_path: Path):
        model_file = tmp_path / "model.joblib"
        model_file.write_bytes(b"fake")
        with pytest.raises(ModelArtifactError, match="Manifest not found"):
            verify_artifact(model_file, tmp_path / "missing.json")

    def test_verify_artifact_missing_model(self, tmp_path: Path):
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps({"sha256": "abc", "size_bytes": 4}))
        with pytest.raises(ModelArtifactError, match="Model file not found"):
            verify_artifact(tmp_path / "missing.joblib", manifest_file)

    def test_verify_artifact_sha_mismatch(self, tmp_path: Path):
        model_file = tmp_path / "model.joblib"
        model_file.write_bytes(b"fake model data")
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(
            json.dumps({"sha256": "0000000000000000", "size_bytes": model_file.stat().st_size})
        )
        with pytest.raises(ModelArtifactError, match="SHA-256 mismatch"):
            verify_artifact(model_file, manifest_file)

    def test_verify_artifact_size_mismatch(self, tmp_path: Path):
        model_file = tmp_path / "model.joblib"
        model_file.write_bytes(b"fake model data")
        real_sha = _sha256(model_file)
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps({"sha256": real_sha, "size_bytes": 9999}))
        with pytest.raises(ModelArtifactError, match="Size mismatch"):
            verify_artifact(model_file, manifest_file)

    def test_verify_artifact_success(self, tmp_path: Path):
        model_file = tmp_path / "model.joblib"
        model_file.write_bytes(b"fake model data")
        real_sha = _sha256(model_file)
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(
            json.dumps({"sha256": real_sha, "size_bytes": model_file.stat().st_size})
        )
        result = verify_artifact(model_file, manifest_file)
        assert result["sha256"] == real_sha

    def test_load_model_type_mismatch(self, tmp_path: Path):
        import joblib

        model_file = tmp_path / "model.joblib"
        joblib.dump(SimpleNamespace(), model_file)
        real_sha = _sha256(model_file)
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(
            json.dumps(
                {
                    "sha256": real_sha,
                    "size_bytes": model_file.stat().st_size,
                    "algorithm": "HistGradientBoostingClassifier",
                }
            )
        )
        with pytest.raises(ModelArtifactError, match="Model type mismatch"):
            load_model(model_file, manifest_file)

    def test_load_model_success_no_algorithm_check(self, tmp_path: Path):
        import joblib

        model_file = tmp_path / "model.joblib"
        joblib.dump(SimpleNamespace(), model_file)
        real_sha = _sha256(model_file)
        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(
            json.dumps({"sha256": real_sha, "size_bytes": model_file.stat().st_size})
        )
        result = load_model(model_file, manifest_file)
        assert result is not None


class TestObesityPredictor:
    def _make_model(self, return_value):
        class FakeModel:
            def predict(self, X):
                return return_value

        return FakeModel()

    def test_predict_returns_class_label(self):
        model = self._make_model(np.array([1]))
        predictor = ObesityPredictor(model)
        result = predictor.predict(SAMPLE_COMMAND)
        assert result == CLASS_MAP[1]

    def test_predict_all_classes(self):
        for code, label in CLASS_MAP.items():
            model = self._make_model(np.array([code]))
            predictor = ObesityPredictor(model)
            assert predictor.predict(SAMPLE_COMMAND) == label

    def test_predict_unknown_code_raises(self):
        model = self._make_model(np.array([99]))
        predictor = ObesityPredictor(model)
        with pytest.raises(PredictionError, match="Unknown prediction code"):
            predictor.predict(SAMPLE_COMMAND)

    def test_predict_unexpected_shape_raises(self):
        model = self._make_model(np.array([1, 2]))
        predictor = ObesityPredictor(model)
        with pytest.raises(PredictionError, match="unexpected output shape"):
            predictor.predict(SAMPLE_COMMAND)

    def test_predict_none_raises(self):
        model = self._make_model(None)
        predictor = ObesityPredictor(model)
        with pytest.raises(PredictionError, match="unexpected output shape"):
            predictor.predict(SAMPLE_COMMAND)
