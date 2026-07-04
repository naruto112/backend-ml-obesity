"""Transform the 12 API input fields into the 15-feature DataFrame expected by the model."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import pandas as pd

ORDINAL_MAP: dict[str, int] = {
    "no": 0,
    "somentimes": 1,
    "frequently": 2,
    "always": 3,
}

FEATURE_COLUMNS: list[str] = [
    "Age",
    "FCVC",
    "NCP",
    "CAEC",
    "CH2O",
    "FAF",
    "TUE",
    "CALC",
    "Gender_Male",
    "family_history_yes",
    "FAVC_yes",
    "MTRANS_Bike",
    "MTRANS_Motorbike",
    "MTRANS_Public_Transportation",
    "MTRANS_Walking",
]

MTRANS_FEATURES: dict[str, str] = {
    "bike": "MTRANS_Bike",
    "motorbike": "MTRANS_Motorbike",
    "public_transportation": "MTRANS_Public_Transportation",
    "walking": "MTRANS_Walking",
}


class FeatureTransformer:
    """Convert a validated API command (12 fields) into a single-row DataFrame with 15 features."""

    def transform(self, command: Mapping[str, Any]) -> pd.DataFrame:
        transport = str(command["meio_transporte"])

        row: dict[str, int | float] = {
            "Age": int(command["idade"]),
            "FCVC": int(command["come_vegetaiis"]),
            "NCP": int(command["refeicoes_diariamente"]),
            "CAEC": ORDINAL_MAP[str(command["come_entre_refeicao"])],
            "CH2O": int(command["litro_agua"]),
            "FAF": int(command["frequencia_semanal_atvidade_fisica"]),
            "TUE": int(command["horas_dispositivo_eletronico"]),
            "CALC": ORDINAL_MAP[str(command["consome_bebida_alcoolica"])],
            "Gender_Male": 1 if int(command["sexo_biologico"]) == 1 else 0,
            "family_history_yes": 1 if str(command["historico_familiar"]) == "yes" else 0,
            "FAVC_yes": 1 if str(command["alimentos_calorico"]) == "yes" else 0,
            "MTRANS_Bike": 1 if transport == "bike" else 0,
            "MTRANS_Motorbike": 1 if transport == "motorbike" else 0,
            "MTRANS_Public_Transportation": 1 if transport == "public_transportation" else 0,
            "MTRANS_Walking": 1 if transport == "walking" else 0,
        }

        return pd.DataFrame([row], columns=FEATURE_COLUMNS)
