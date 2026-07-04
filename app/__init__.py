"""Flask application factory."""

from flask import Flask

from app.api.domain_routes import domain_blueprint
from app.api.errors import register_error_handlers
from app.api.health_routes import health_blueprint
from app.api.middleware import configure_logging, register_request_middleware
from app.api.obesity_record_routes import record_blueprint
from app.config import load_config
from app.extensions import api, db
from app.schemas import ObesityRecordCreateSchema


def create_app(config_name: str | None = None) -> Flask:
    """Create the Flask application without touching external resources.

    Building the application never runs migrations, seeds, or database queries.
    """
    app = Flask(__name__)
    app.config.from_mapping(load_config(config_name))
    configure_logging(app)
    db.init_app(app)
    api.init_app(app)
    api.spec.components.schema("ObesityRecordCreate", schema=ObesityRecordCreateSchema)
    api.register_blueprint(health_blueprint)
    api.register_blueprint(domain_blueprint)
    api.register_blueprint(record_blueprint)
    register_request_middleware(app)
    register_error_handlers(app)

    # Register model metadata for Alembic without touching the database.
    from app import models  # noqa: F401

    return app


__all__ = ["create_app"]
