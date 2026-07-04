"""Process and database health endpoints."""

from flask import Response, jsonify
from flask_smorest import Blueprint  # type: ignore[import-untyped]
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.schemas import StatusSchema

health_blueprint = Blueprint(
    "health", "health", url_prefix="/health", description="Process and dependency health"
)


@health_blueprint.get("/live")
@health_blueprint.response(200, StatusSchema)
def liveness() -> tuple[Response, int]:
    return jsonify({"status": "ok"}), 200


@health_blueprint.get("/ready")
@health_blueprint.response(200, StatusSchema)
@health_blueprint.alt_response(503, schema=StatusSchema, description="Database unavailable")
def readiness() -> tuple[Response, int]:
    try:
        db.session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"status": "unavailable"}), 503
    return jsonify({"status": "ok"}), 200
