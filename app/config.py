"""Environment-based application configuration."""

from __future__ import annotations

import os
from typing import ClassVar


class ConfigurationError(RuntimeError):
    """Raised when the process cannot start with the supplied configuration."""


class BaseConfig:
    DEBUG: ClassVar[bool] = False
    TESTING: ClassVar[bool] = False
    SQLALCHEMY_TRACK_MODIFICATIONS: ClassVar[bool] = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    """Tests provide a PostgreSQL URL; creating the app does not connect to it."""

    TESTING = True


class ProductionConfig(BaseConfig):
    pass


CONFIG_BY_NAME: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def _resolve_environment(config_name: str | None) -> str:
    environment = config_name if config_name is not None else os.getenv("APP_ENV")
    if environment is None or not environment.strip():
        raise ConfigurationError("APP_ENV is required")

    normalized_environment = environment.strip().lower()
    if normalized_environment not in CONFIG_BY_NAME:
        supported = ", ".join(sorted(CONFIG_BY_NAME))
        raise ConfigurationError(f"APP_ENV must be one of: {supported}")

    return normalized_environment


def _required_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url is None or not database_url.strip():
        raise ConfigurationError("DATABASE_URL is required")

    return database_url.strip()


def _integer_setting(name: str, default: int, *, minimum: int = 1) -> int:
    raw_value = os.getenv(name)
    if raw_value is None or not raw_value.strip():
        return default

    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer") from exc

    if value < minimum:
        raise ConfigurationError(f"{name} must be at least {minimum}")
    return value


def load_config(config_name: str | None = None) -> dict[str, object]:
    """Build Flask configuration without creating a database engine."""
    environment = _resolve_environment(config_name)
    config_type = CONFIG_BY_NAME[environment]
    database_url = _required_database_url()

    return {
        "APP_ENV": environment,
        "DATABASE_URL": database_url,
        "DEBUG": config_type.DEBUG,
        "TESTING": config_type.TESTING,
        "SQLALCHEMY_DATABASE_URI": database_url,
        "SQLALCHEMY_TRACK_MODIFICATIONS": (config_type.SQLALCHEMY_TRACK_MODIFICATIONS),
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "pool_size": _integer_setting("DB_POOL_SIZE", 5),
            "max_overflow": _integer_setting("DB_MAX_OVERFLOW", 10, minimum=0),
            "pool_timeout": _integer_setting("DB_POOL_TIMEOUT", 10),
            "pool_recycle": _integer_setting("DB_POOL_RECYCLE", 1800),
            "pool_pre_ping": True,
        },
        "MAX_CONTENT_LENGTH": _integer_setting("MAX_CONTENT_LENGTH", 64 * 1024),
        "READINESS_TIMEOUT": _integer_setting("READINESS_TIMEOUT", 2),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO",
        "API_TITLE": "Obesity Data API",
        "API_VERSION": "v1",
        "OPENAPI_VERSION": "3.0.3",
        "OPENAPI_URL_PREFIX": "/api",
        "OPENAPI_JSON_PATH": "openapi.json",
        "OPENAPI_SWAGGER_UI_PATH": "docs",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
    }


__all__ = [
    "BaseConfig",
    "ConfigurationError",
    "DevelopmentConfig",
    "ProductionConfig",
    "TestingConfig",
    "load_config",
]
