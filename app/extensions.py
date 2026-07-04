"""Application extensions initialized by the factory."""

from flask_smorest import Api  # type: ignore[import-untyped]
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"expire_on_commit": False})
api = Api()


__all__ = ["api", "db"]
