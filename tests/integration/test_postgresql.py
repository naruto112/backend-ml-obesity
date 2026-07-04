from __future__ import annotations

import os
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import DomainField, DomainOption, ObesityRecord
from app.repositories import DomainRepository, ObesityRecordRepository
from seeds.domain_options import seed

DATABASE_URL = os.getenv("DATABASE_URL", "")
pytestmark = pytest.mark.skipif(
    os.getenv("RUN_POSTGRES_TESTS") != "1",
    reason="set RUN_POSTGRES_TESTS=1 with a disposable PostgreSQL database",
)


def test_ct_db_seed_is_idempotent_and_catalog_is_complete() -> None:
    seed(DATABASE_URL)
    seed(DATABASE_URL)
    engine = create_engine(DATABASE_URL)
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(DomainField)) == 12
        assert session.scalar(select(func.count()).select_from(DomainOption)) == 45
        domains = DomainRepository(session).list_active_with_options()
        assert len(domains) == 12
        assert domains[0].name == "sexo_biologico"
        assert domains[0].options[0].value == "1"
    engine.dispose()


def test_ct_db_record_round_trip_and_check_constraint() -> None:
    engine = create_engine(DATABASE_URL)
    valid = {
        "idade": 35,
        "sexo_biologico": 1,
        "come_vegetaiis": 2,
        "refeicoes_diariamente": 3,
        "come_entre_refeicao": "somentimes",
        "litro_agua": 2,
        "frequencia_semanal_atvidade_fisica": 2,
        "horas_dispositivo_eletronico": 1,
        "consome_bebida_alcoolica": "no",
        "historico_familiar": "yes",
        "alimentos_calorico": "no",
        "meio_transporte": "public_transportation",
        "obesity": "Normal_Weight",
    }
    with Session(engine, expire_on_commit=False) as session:
        repository = ObesityRecordRepository(session)
        record = repository.add(valid)
        session.commit()
        assert repository.get_by_id(record.id).idade == 35  # type: ignore[union-attr]

        invalid = ObesityRecord(id=uuid4(), **{**valid, "idade": 121})
        session.add(invalid)
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()
    engine.dispose()
