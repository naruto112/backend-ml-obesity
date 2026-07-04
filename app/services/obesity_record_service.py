"""Obesity record use cases and transaction boundary."""

from collections.abc import Mapping
from typing import Any, Protocol
from uuid import UUID

from app.repositories import ObesityRecordRepository


class Transaction(Protocol):
    def commit(self) -> None: ...

    def rollback(self) -> None: ...


class ObesityRecordNotFoundError(LookupError):
    pass


class ObesityRecordService:
    def __init__(
        self,
        repository: ObesityRecordRepository,
        transaction: Transaction,
    ) -> None:
        self._repository = repository
        self._transaction = transaction

    def create_record(self, command: Mapping[str, Any]) -> Any:
        try:
            record = self._repository.add(command)
            self._transaction.commit()
            return record
        except Exception:
            self._transaction.rollback()
            raise

    def get_record(self, record_id: UUID) -> Any:
        record = self._repository.get_by_id(record_id)
        if record is None:
            raise ObesityRecordNotFoundError(str(record_id))
        return record
