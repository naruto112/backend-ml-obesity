"""Obesity record HTTP routes."""

from typing import Any
from uuid import UUID

from flask import current_app, request, url_for
from flask.views import MethodView
from flask_smorest import Blueprint  # type: ignore[import-untyped]
from marshmallow import ValidationError

from app.api.errors import problem_response, validation_problem
from app.domain_catalog import RECORD_FIELDS
from app.extensions import db
from app.repositories import ObesityRecordRepository
from app.schemas import ObesityRecordCreatedSchema, ObesityRecordReadSchema
from app.schemas.obesity_record_schema import ObesityRecordCreateSchema
from app.services import ObesityRecordService

record_blueprint = Blueprint(
    "obesity-records",
    "obesity-records",
    url_prefix="/api/v1/obesity-records",
    description="Obesity form records",
)


def _service() -> ObesityRecordService:
    predictor = current_app.config["ML_PREDICTOR"]
    return ObesityRecordService(ObesityRecordRepository(db.session), db.session, predictor)


def _isoformat(value: Any) -> str:
    return str(value.isoformat()).replace("+00:00", "Z")


def _serialize_record(record: Any) -> dict[str, Any]:
    result = {field: getattr(record, field) for field in RECORD_FIELDS}
    result.update({"id": record.id, "created_at": _isoformat(record.created_at)})
    return result


@record_blueprint.route("")
class ObesityRecordCollection(MethodView):
    @record_blueprint.doc(
        requestBody={
            "required": True,
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/ObesityRecordCreate"}}
            },
        },
        responses={
            "400": {"description": "Empty or malformed JSON"},
            "413": {"description": "Body exceeds 64 KiB"},
            "415": {"description": "Content-Type is not JSON"},
            "422": {"description": "Payload validation failed"},
            "500": {"description": "Internal error"},
        },
    )
    @record_blueprint.response(201, ObesityRecordCreatedSchema)
    def post(self) -> Any:
        if not request.is_json:
            return problem_response(
                415, "unsupported-media-type", "Midia nao suportada", "Use application/json."
            )
        if not request.get_data(cache=True):
            return problem_response(
                400, "invalid-json", "JSON invalido", "O corpo JSON esta vazio ou malformado."
            )
        payload = request.get_json()
        if not isinstance(payload, dict):
            return validation_problem({"$": ["invalid_type"]})
        try:
            command = ObesityRecordCreateSchema().load(payload)
        except ValidationError as error:
            messages = error.messages
            if not isinstance(messages, dict):
                messages = {"$": ["invalid_type"]}
            return validation_problem(messages)

        record = _service().create_record(command)
        location = url_for("obesity-records.ObesityRecordItem", record_id=record.id)
        return (
            {"id": record.id, "created_at": _isoformat(record.created_at)},
            201,
            {"Location": location},
        )


@record_blueprint.route("/<string:record_id>")
class ObesityRecordItem(MethodView):
    @record_blueprint.doc(
        responses={
            "400": {"description": "Malformed UUID"},
            "404": {"description": "Record not found"},
            "500": {"description": "Internal error"},
        }
    )
    @record_blueprint.response(200, ObesityRecordReadSchema)
    def get(self, record_id: str) -> Any:
        try:
            parsed_id = UUID(record_id)
        except ValueError:
            return problem_response(
                400, "invalid-uuid", "UUID invalido", "O identificador nao e um UUID valido."
            )
        return _serialize_record(_service().get_record(parsed_id))
