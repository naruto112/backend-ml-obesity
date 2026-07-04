"""Domain catalog HTTP routes."""

from flask.views import MethodView
from flask_smorest import Blueprint  # type: ignore[import-untyped]

from app.extensions import db
from app.repositories import DomainRepository
from app.schemas import DomainFieldSchema, DomainListSchema
from app.services import DomainService

domain_blueprint = Blueprint(
    "domains", "domains", url_prefix="/api/v1/domains", description="Form domains"
)


def _service() -> DomainService:
    return DomainService(DomainRepository(db.session))


@domain_blueprint.route("")
class DomainCollection(MethodView):
    @domain_blueprint.response(200, DomainListSchema)
    def get(self) -> dict[str, object]:
        return {"data": _service().list_active_domains()}


@domain_blueprint.route("/<string:field_name>")
class DomainItem(MethodView):
    @domain_blueprint.alt_response(404, description="Domain not found")
    @domain_blueprint.response(200, DomainFieldSchema)
    def get(self, field_name: str) -> dict[str, object]:
        return _service().get_active_domain(field_name)
