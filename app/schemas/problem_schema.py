"""Problem details response schemas."""

from marshmallow import Schema, fields


class ProblemErrorSchema(Schema):
    field = fields.String(required=True)
    code = fields.String(required=True)
    message = fields.String(required=True)


class ProblemSchema(Schema):
    type = fields.String(required=True)
    title = fields.String(required=True)
    status = fields.Integer(required=True)
    detail = fields.String(required=True)
    instance = fields.String(required=True)
    request_id = fields.String(required=True)
    errors = fields.List(fields.Nested(ProblemErrorSchema), required=False)


__all__ = ["ProblemErrorSchema", "ProblemSchema"]
