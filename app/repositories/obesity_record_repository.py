"""Persistence operations for obesity records."""

from collections.abc import Mapping
from typing import Any, cast
from uuid import UUID

from sqlalchemy import select

from app.models import ObesityRecord


class ObesityRecordRepository:
    def __init__(self, session: Any) -> None:
        self._session = session

    def add(self, values: Mapping[str, Any]) -> ObesityRecord:
        record = ObesityRecord(**values)
        self._session.add(record)
        self._session.flush()
        return record

    def get_by_id(self, record_id: UUID) -> ObesityRecord | None:
        return cast(ObesityRecord | None, self._session.get(ObesityRecord, record_id))

    def list_all(self) -> list[ObesityRecord]:
        statement = select(ObesityRecord).order_by(
            ObesityRecord.created_at.desc(), ObesityRecord.id.desc()
        )
        return list(self._session.scalars(statement))
