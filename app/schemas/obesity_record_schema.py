"""Schemas for obesity record commands."""

from marshmallow import RAISE, Schema, fields, validate

from app.domain_catalog import DOMAIN_VALUES, OBESITY_CLASSES
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
    """Validate the exact 12-field v1 input contract (obesity is server-derived)."""

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


class ObesityRecordCreatedSchema(Schema):
    id = fields.UUID(required=True)
    created_at = fields.String(required=True)


class ObesityRecordReadSchema(Schema):
    """Read schema with all 13 fields: 12 inputs + server-derived obesity."""

    id = fields.UUID(required=True)
    created_at = fields.String(required=True)

    idade = StrictInteger(required=True)
    sexo_biologico = StrictInteger(required=True)
    come_vegetaiis = StrictInteger(required=True)
    refeicoes_diariamente = StrictInteger(required=True)
    come_entre_refeicao = StrictString(required=True)
    litro_agua = StrictInteger(required=True)
    frequencia_semanal_atvidade_fisica = StrictInteger(required=True)
    horas_dispositivo_eletronico = StrictInteger(required=True)
    consome_bebida_alcoolica = StrictString(required=True)
    historico_familiar = StrictString(required=True)
    alimentos_calorico = StrictString(required=True)
    meio_transporte = StrictString(required=True)
    obesity = StrictString(
        required=True,
        validate=validate.OneOf(OBESITY_CLASSES, error="invalid_domain"),
    )


class PageQuerySchema(Schema):
    """Validate pagination query-string parameters."""

    page = fields.Integer(load_default=1, validate=validate.Range(min=1, error="out_of_range"))
    per_page = fields.Integer(
        load_default=10, validate=validate.Range(min=1, max=100, error="out_of_range")
    )


class PaginationMetaSchema(Schema):
    page = fields.Integer(required=True)
    per_page = fields.Integer(required=True)
    total = fields.Integer(required=True)
    total_pages = fields.Integer(required=True)
    has_next = fields.Boolean(required=True)
    has_prev = fields.Boolean(required=True)


class ObesityRecordPageSchema(Schema):
    """Paginated collection of obesity records."""

    data = fields.List(fields.Nested(ObesityRecordReadSchema), required=True)
    pagination = fields.Nested(PaginationMetaSchema, required=True)


__all__ = [
    "ObesityRecordCreateSchema",
    "ObesityRecordCreatedSchema",
    "ObesityRecordPageSchema",
    "ObesityRecordReadSchema",
    "PageQuerySchema",
    "PaginationMetaSchema",
]
