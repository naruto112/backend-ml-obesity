from __future__ import annotations

from uuid import uuid4

from app.models import ObesityRecord
from app.repositories import DomainRepository, ObesityRecordRepository


class ScalarResultStub:
    def __init__(self, values):
        self.values = values

    def unique(self):
        return self

    def __iter__(self):
        return iter(self.values)


class SessionStub:
    def __init__(self) -> None:
        self.added = None
        self.flushed = False
        self.scalar_value = None
        self.get_value = None

    def scalars(self, statement):
        return ScalarResultStub(["field"])

    def scalar(self, statement):
        return self.scalar_value

    def add(self, value) -> None:
        self.added = value

    def flush(self) -> None:
        self.flushed = True

    def get(self, model, identifier):
        return self.get_value


def test_domain_repository_executes_list_and_item_queries() -> None:
    session = SessionStub()
    repository = DomainRepository(session)

    assert repository.list_active_with_options() == ["field"]
    assert repository.get_active_by_name("sexo_biologico") is None


def test_record_repository_adds_flushes_and_reads() -> None:
    session = SessionStub()
    repository = ObesityRecordRepository(session)
    values = {
        "idade": 35,
        "sexo_biologico": 1,
        "come_vegetaiis": 2,
        "refeicoes_diariamente": 3,
        "come_entre_refeicao": "no",
        "litro_agua": 2,
        "frequencia_semanal_atvidade_fisica": 2,
        "horas_dispositivo_eletronico": 1,
        "consome_bebida_alcoolica": "no",
        "historico_familiar": "yes",
        "alimentos_calorico": "no",
        "meio_transporte": "walking",
        "obesity": "Normal_Weight",
    }

    record = repository.add(values)
    session.get_value = record

    assert isinstance(record, ObesityRecord)
    assert session.added is record
    assert session.flushed is True
    assert repository.get_by_id(uuid4()) is record


def test_record_repository_lists_all() -> None:
    repository = ObesityRecordRepository(SessionStub())

    assert repository.list_all() == ["field"]
