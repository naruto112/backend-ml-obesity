from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.services import (
    DomainNotFoundError,
    DomainService,
    ObesityRecordNotFoundError,
    ObesityRecordService,
)


class DomainRepositoryStub:
    def __init__(self, fields: list[SimpleNamespace]) -> None:
        self.fields = fields

    def list_active_with_options(self):
        return self.fields

    def get_active_by_name(self, name: str):
        return next((field for field in self.fields if field.name == name), None)


class RecordRepositoryStub:
    def __init__(self, record=None, error: Exception | None = None) -> None:
        self.record = record
        self.error = error
        self.added = None

    def add(self, values):
        if self.error is not None:
            raise self.error
        self.added = values
        return self.record

    def get_by_id(self, record_id):
        return self.record


class TransactionStub:
    def __init__(self) -> None:
        self.commits = 0
        self.rollbacks = 0

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1


def test_domain_service_orders_and_converts_integer_options() -> None:
    field = SimpleNamespace(
        name="sexo_biologico",
        label="Sexo biologico",
        data_type="integer",
        required=True,
        options=[SimpleNamespace(value="1", label="Masculino", display_order=1)],
    )
    service = DomainService(DomainRepositoryStub([field]))  # type: ignore[arg-type]

    result = service.list_active_domains()

    assert result[0]["options"][0]["value"] == 1
    assert service.get_active_domain("sexo_biologico") == result[0]


def test_domain_service_preserves_string_options() -> None:
    field = SimpleNamespace(
        name="historico_familiar",
        label="Historico",
        data_type="string",
        required=True,
        options=[SimpleNamespace(value="yes", label="Sim", display_order=1)],
    )
    service = DomainService(DomainRepositoryStub([field]))  # type: ignore[arg-type]

    assert service.list_active_domains()[0]["options"][0]["value"] == "yes"


def test_domain_service_raises_not_found() -> None:
    service = DomainService(DomainRepositoryStub([]))  # type: ignore[arg-type]
    with pytest.raises(DomainNotFoundError):
        service.get_active_domain("unknown")


def test_record_service_commits_successful_create() -> None:
    record = SimpleNamespace(id=uuid4())
    repository = RecordRepositoryStub(record)
    transaction = TransactionStub()
    service = ObesityRecordService(repository, transaction)  # type: ignore[arg-type]

    assert service.create_record({"idade": 35}) is record
    assert repository.added == {"idade": 35}
    assert transaction.commits == 1
    assert transaction.rollbacks == 0


def test_record_service_rolls_back_failed_create() -> None:
    repository = RecordRepositoryStub(error=RuntimeError("database failed"))
    transaction = TransactionStub()
    service = ObesityRecordService(repository, transaction)  # type: ignore[arg-type]

    with pytest.raises(RuntimeError, match="database failed"):
        service.create_record({"idade": 35})
    assert transaction.commits == 0
    assert transaction.rollbacks == 1


def test_record_service_reads_or_raises_not_found() -> None:
    record = SimpleNamespace(id=uuid4())
    transaction = TransactionStub()
    service = ObesityRecordService(  # type: ignore[arg-type]
        RecordRepositoryStub(record), transaction
    )
    assert service.get_record(record.id) is record

    missing = ObesityRecordService(  # type: ignore[arg-type]
        RecordRepositoryStub(), transaction
    )
    with pytest.raises(ObesityRecordNotFoundError):
        missing.get_record(uuid4())
