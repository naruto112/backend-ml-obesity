from __future__ import annotations

import pytest

from app import create_app


@pytest.fixture
def app(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@invalid/test")
    return create_app()


def test_ct_contrato_openapi_contains_all_routes_and_input_schema(app) -> None:
    document = app.test_client().get("/api/openapi.json").get_json()
    assert set(document["paths"]) == {
        "/health/live",
        "/health/ready",
        "/api/v1/domains",
        "/api/v1/domains/{field_name}",
        "/api/v1/obesity-records",
        "/api/v1/obesity-records/{record_id}",
    }
    create = document["components"]["schemas"]["ObesityRecordCreate"]
    assert len(create["required"]) == 13
    post = document["paths"]["/api/v1/obesity-records"]["post"]
    assert post["requestBody"]["required"] is True
    assert {"201", "400", "413", "415", "422", "500"}.issubset(post["responses"])
