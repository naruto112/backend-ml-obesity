from __future__ import annotations

from flask import Flask

from app import create_app


def test_factory_registers_sqlalchemy_without_connecting(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://test:test@database-that-does-not-exist/test",
    )

    app = create_app()

    assert isinstance(app, Flask)
    assert app.testing is True
    assert "sqlalchemy" in app.extensions


def test_factory_creates_isolated_instances(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@invalid/test")

    first = create_app()
    second = create_app()

    assert first is not second
    assert first.config is not second.config
    assert first.extensions["sqlalchemy"] is second.extensions["sqlalchemy"]
