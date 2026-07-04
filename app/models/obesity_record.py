"""Obesity form response model."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Index, SmallInteger, String, func
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class ObesityRecord(db.Model):  # type: ignore[name-defined]
    __tablename__ = "obesity_record"
    __table_args__ = (
        CheckConstraint("idade BETWEEN 1 AND 120", name="ck_record_idade"),
        CheckConstraint("sexo_biologico IN (1, 2)", name="ck_record_sexo"),
        CheckConstraint("come_vegetaiis IN (1, 2, 3)", name="ck_record_vegetais"),
        CheckConstraint("refeicoes_diariamente IN (1, 2, 3, 4, 5)", name="ck_record_refeicoes"),
        CheckConstraint(
            "come_entre_refeicao IN ('no', 'somentimes', 'frequently', 'always')",
            name="ck_record_entre_refeicao",
        ),
        CheckConstraint("litro_agua IN (1, 2, 3)", name="ck_record_agua"),
        CheckConstraint(
            "frequencia_semanal_atvidade_fisica IN (0, 1, 2, 3, 4)",
            name="ck_record_atividade",
        ),
        CheckConstraint(
            "horas_dispositivo_eletronico IN (0, 1, 2)",
            name="ck_record_dispositivo",
        ),
        CheckConstraint(
            "consome_bebida_alcoolica IN ('no', 'somentimes', 'frequently', 'always')",
            name="ck_record_alcool",
        ),
        CheckConstraint("historico_familiar IN ('yes', 'no')", name="ck_record_historico"),
        CheckConstraint("alimentos_calorico IN ('yes', 'no')", name="ck_record_calorico"),
        CheckConstraint(
            "meio_transporte IN ('automobile', 'motorbike', 'bike', "
            "'public_transportation', 'walking')",
            name="ck_record_transporte",
        ),
        CheckConstraint(
            "obesity IN ('Insufficient_Weight', 'Normal_Weight', "
            "'Overweight_Level_I', 'Overweight_Level_II', 'Obesity_Type_I', "
            "'Obesity_Type_II', 'Obesity_Type_III')",
            name="ck_record_obesity",
        ),
        Index("ix_obesity_record_created_at", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True, default=uuid4)
    idade: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    sexo_biologico: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    come_vegetaiis: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    refeicoes_diariamente: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    come_entre_refeicao: Mapped[str] = mapped_column(String(16), nullable=False)
    litro_agua: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    frequencia_semanal_atvidade_fisica: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    horas_dispositivo_eletronico: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    consome_bebida_alcoolica: Mapped[str] = mapped_column(String(16), nullable=False)
    historico_familiar: Mapped[str] = mapped_column(String(3), nullable=False)
    alimentos_calorico: Mapped[str] = mapped_column(String(3), nullable=False)
    meio_transporte: Mapped[str] = mapped_column(String(32), nullable=False)
    obesity: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
