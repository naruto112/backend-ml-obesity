"""Canonical v1 field names and accepted domain values."""

from __future__ import annotations

from types import MappingProxyType
from typing import Final, Literal

DomainType = Literal["integer", "string"]

INPUT_FIELDS: Final[tuple[str, ...]] = (
    "idade",
    "sexo_biologico",
    "come_vegetaiis",
    "refeicoes_diariamente",
    "come_entre_refeicao",
    "litro_agua",
    "frequencia_semanal_atvidade_fisica",
    "horas_dispositivo_eletronico",
    "consome_bebida_alcoolica",
    "historico_familiar",
    "alimentos_calorico",
    "meio_transporte",
)

RECORD_FIELDS: Final[tuple[str, ...]] = INPUT_FIELDS + ("obesity",)

OBESITY_CLASSES: Final[tuple[str, ...]] = (
    "Insufficient_Weight",
    "Normal_Weight",
    "Obesity_Type_I",
    "Obesity_Type_II",
    "Obesity_Type_III",
    "Overweight_Level_I",
    "Overweight_Level_II",
)

DOMAIN_VALUES = MappingProxyType(
    {
        "sexo_biologico": (1, 2),
        "come_vegetaiis": (1, 2, 3),
        "refeicoes_diariamente": (1, 2, 3, 4, 5),
        "come_entre_refeicao": ("no", "somentimes", "frequently", "always"),
        "litro_agua": (1, 2, 3),
        "frequencia_semanal_atvidade_fisica": (0, 1, 2, 3, 4),
        "horas_dispositivo_eletronico": (0, 1, 2),
        "consome_bebida_alcoolica": ("no", "somentimes", "frequently", "always"),
        "historico_familiar": ("yes", "no"),
        "alimentos_calorico": ("yes", "no"),
        "meio_transporte": (
            "automobile",
            "motorbike",
            "bike",
            "public_transportation",
            "walking",
        ),
        "obesity": OBESITY_CLASSES,
    }
)


__all__ = [
    "DOMAIN_VALUES",
    "DomainType",
    "INPUT_FIELDS",
    "OBESITY_CLASSES",
    "RECORD_FIELDS",
]
