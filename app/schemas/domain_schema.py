"""Domain catalog response schemas."""

from marshmallow import Schema, fields


class DomainOptionSchema(Schema):
    value = fields.Raw(required=True)
    label = fields.String(required=True)
    order = fields.Integer(required=True)


class DomainFieldSchema(Schema):
    field = fields.String(required=True)
    label = fields.String(required=True)
    type = fields.String(required=True)
    required = fields.Boolean(required=True)
    options = fields.List(fields.Nested(DomainOptionSchema), required=True)


class DomainListSchema(Schema):
    data = fields.List(fields.Nested(DomainFieldSchema), required=True)


class StatusSchema(Schema):
    status = fields.String(required=True)


__all__ = ["DomainFieldSchema", "DomainListSchema", "DomainOptionSchema", "StatusSchema"]
