"""Queries for the active domain catalog."""

from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import DomainField, DomainOption


class DomainRepository:
    def __init__(self, session: Any) -> None:
        self._session = session

    def list_active_with_options(self) -> list[DomainField]:
        statement = (
            select(DomainField)
            .where(DomainField.active.is_(True))
            .options(selectinload(DomainField.options.and_(DomainOption.active.is_(True))))
            .order_by(DomainField.display_order)
        )
        return list(self._session.scalars(statement).unique())

    def get_active_by_name(self, name: str) -> DomainField | None:
        statement = (
            select(DomainField)
            .where(DomainField.name == name, DomainField.active.is_(True))
            .options(selectinload(DomainField.options.and_(DomainOption.active.is_(True))))
        )
        return cast(DomainField | None, self._session.scalar(statement))
