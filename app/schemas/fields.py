"""Marshmallow fields that do not coerce JSON values."""

from typing import Any

from marshmallow import ValidationError, fields


class StrictInteger(fields.Integer):
    """Accept JSON integers while rejecting booleans and coercible values."""

    def _deserialize(
        self,
        value: Any,
        attr: str | None,
        data: Any,
        **kwargs: Any,
    ) -> int:
        if type(value) is not int:
            raise ValidationError("invalid_type")
        return value


class StrictString(fields.String):
    """Accept only native JSON strings without coercion."""

    def _deserialize(
        self,
        value: Any,
        attr: str | None,
        data: Any,
        **kwargs: Any,
    ) -> str:
        if type(value) is not str:
            raise ValidationError("invalid_type")
        return value


__all__ = ["StrictInteger", "StrictString"]
