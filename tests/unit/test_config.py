from __future__ import annotations

import pytest

from app.config import ConfigurationError, load_config


def test_load_config_requires_app_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@invalid/test")

    with pytest.raises(ConfigurationError, match="APP_ENV is required"):
        load_config()


def test_load_config_requires_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ConfigurationError, match="DATABASE_URL is required"):
        load_config()


def test_explicit_environment_has_precedence(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@invalid/test")

    config = load_config(" TESTING ")

    assert config["APP_ENV"] == "testing"
    assert config["TESTING"] is True
    assert config["DEBUG"] is False
    assert config["MAX_CONTENT_LENGTH"] == 65536


@pytest.mark.parametrize("value", ["unknown", " "])
def test_invalid_environment_is_rejected(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("APP_ENV", value)
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@invalid/test")

    with pytest.raises(ConfigurationError):
        load_config()


def test_invalid_numeric_setting_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@invalid/test")
    monkeypatch.setenv("DB_POOL_SIZE", "zero")

    with pytest.raises(ConfigurationError, match="DB_POOL_SIZE must be an integer"):
        load_config()


def test_numeric_setting_below_minimum_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://test:test@invalid/test")
    monkeypatch.setenv("DB_POOL_SIZE", "0")

    with pytest.raises(ConfigurationError, match="DB_POOL_SIZE must be at least 1"):
        load_config()
