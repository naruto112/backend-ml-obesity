from __future__ import annotations

from copy import deepcopy
from typing import Any

import pytest
from marshmallow import ValidationError

from app.domain_catalog import DOMAIN_VALUES, RECORD_FIELDS
from app.schemas import ObesityRecordCreateSchema


@pytest.fixture
def valid_payload() -> dict[str, Any]:
    return {
        "idade": 35,
        "sexo_biologico": 1,
        "come_vegetaiis": 2,
        "refeicoes_diariamente": 3,
        "come_entre_refeicao": "somentimes",
        "litro_agua": 2,
        "frequencia_semanal_atvidade_fisica": 2,
        "horas_dispositivo_eletronico": 1,
        "consome_bebida_alcoolica": "no",
        "historico_familiar": "yes",
        "alimentos_calorico": "no",
        "meio_transporte": "public_transportation",
        "obesity": "Normal_Weight",
    }


def _assert_error(payload: dict[str, Any], field: str, code: str) -> None:
    with pytest.raises(ValidationError) as raised:
        ObesityRecordCreateSchema().load(payload)
    assert code in raised.value.messages[field]


def test_valid_payload_round_trips(valid_payload: dict[str, Any]) -> None:
    assert ObesityRecordCreateSchema().load(valid_payload) == valid_payload
    assert tuple(valid_payload) == RECORD_FIELDS


@pytest.mark.parametrize("idade", [1, 18, 35, 120])
def test_ct_idade_01_accepts_boundaries(valid_payload: dict[str, Any], idade: int) -> None:
    valid_payload["idade"] = idade
    assert ObesityRecordCreateSchema().load(valid_payload)["idade"] == idade


@pytest.mark.parametrize("idade", [0, -1, 121, 150, 2147483647])
def test_ct_idade_02_03_rejects_out_of_range(valid_payload: dict[str, Any], idade: int) -> None:
    valid_payload["idade"] = idade
    _assert_error(valid_payload, "idade", "out_of_range")


@pytest.mark.parametrize("value", [35.5, "35", True, {}, []])
def test_ct_idade_04_rejects_non_integer_types(valid_payload: dict[str, Any], value: Any) -> None:
    valid_payload["idade"] = value
    _assert_error(valid_payload, "idade", "invalid_type")


@pytest.mark.parametrize("field", RECORD_FIELDS)
def test_null_is_rejected(valid_payload: dict[str, Any], field: str) -> None:
    valid_payload[field] = None
    _assert_error(valid_payload, field, "null_not_allowed")


@pytest.mark.parametrize("field", RECORD_FIELDS)
def test_omitted_field_is_rejected(valid_payload: dict[str, Any], field: str) -> None:
    valid_payload.pop(field)
    _assert_error(valid_payload, field, "required")


@pytest.mark.parametrize(
    ("field", "values"),
    [(field, values) for field, values in DOMAIN_VALUES.items()],
)
def test_each_domain_value_is_accepted(
    valid_payload: dict[str, Any], field: str, values: tuple[Any, ...]
) -> None:
    for value in values:
        payload = deepcopy(valid_payload)
        payload[field] = value
        assert ObesityRecordCreateSchema().load(payload)[field] == value


@pytest.mark.parametrize("field", DOMAIN_VALUES)
def test_value_outside_domain_is_rejected(valid_payload: dict[str, Any], field: str) -> None:
    valid_payload[field] = 999 if isinstance(DOMAIN_VALUES[field][0], int) else "invalid"
    _assert_error(valid_payload, field, "invalid_domain")


@pytest.mark.parametrize("field", DOMAIN_VALUES)
def test_domain_field_rejects_wrong_type(valid_payload: dict[str, Any], field: str) -> None:
    valid_payload[field] = (
        str(DOMAIN_VALUES[field][0]) if isinstance(DOMAIN_VALUES[field][0], int) else 1
    )
    _assert_error(valid_payload, field, "invalid_type")


def test_unknown_field_is_rejected(valid_payload: dict[str, Any]) -> None:
    valid_payload["extra"] = "value"
    _assert_error(valid_payload, "extra", "unknown_field")
