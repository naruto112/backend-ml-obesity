"""Schemas for obesity record commands."""

from marshmallow import RAISE, Schema, fields, validate

from app.domain_catalog import DOMAIN_VALUES
from app.schemas.fields import StrictInteger, StrictString

COMMON_ERRORS = {
    "required": "required",
    "null": "null_not_allowed",
}


def _integer_domain(field_name: str) -> StrictInteger:
    return StrictInteger(
        required=True,
        allow_none=False,
        validate=validate.OneOf(DOMAIN_VALUES[field_name], error="invalid_domain"),
        error_messages=COMMON_ERRORS,
    )


def _string_domain(field_name: str) -> StrictString:
    return StrictString(
        required=True,
        allow_none=False,
        validate=validate.OneOf(DOMAIN_VALUES[field_name], error="invalid_domain"),
        error_messages=COMMON_ERRORS,
    )


class ObesityRecordCreateSchema(Schema):
    """Validate the exact 13-field v1 input contract."""

    error_messages = {"unknown": "unknown_field"}

    class Meta:
        unknown = RAISE

    idade = StrictInteger(
        required=True,
        allow_none=False,
        validate=validate.Range(min=1, max=120, error="out_of_range"),
        error_messages=COMMON_ERRORS,
    )
    sexo_biologico = _integer_domain("sexo_biologico")
    come_vegetaiis = _integer_domain("come_vegetaiis")
    refeicoes_diariamente = _integer_domain("refeicoes_diariamente")
    come_entre_refeicao = _string_domain("come_entre_refeicao")
    litro_agua = _integer_domain("litro_agua")
    frequencia_semanal_atvidade_fisica = _integer_domain("frequencia_semanal_atvidade_fisica")
    horas_dispositivo_eletronico = _integer_domain("horas_dispositivo_eletronico")
    consome_bebida_alcoolica = _string_domain("consome_bebida_alcoolica")
    historico_familiar = _string_domain("historico_familiar")
    alimentos_calorico = _string_domain("alimentos_calorico")
    meio_transporte = _string_domain("meio_transporte")
    obesity = _string_domain("obesity")


class ObesityRecordCreatedSchema(Schema):
    id = fields.UUID(required=True)
    created_at = fields.String(required=True)


class ObesityRecordReadSchema(ObesityRecordCreateSchema):
    id = fields.UUID(required=True)
    created_at = fields.String(required=True)


__all__ = [
    "ObesityRecordCreateSchema",
    "ObesityRecordCreatedSchema",
    "ObesityRecordReadSchema",
]
