"""Upsert the canonical v1 domain catalog."""

# ruff: noqa: E501

from __future__ import annotations

import os
from typing import Any

from sqlalchemy import create_engine, func
from sqlalchemy.dialects.postgresql import insert

from app.models import DomainField, DomainOption

CATALOG: tuple[dict[str, Any], ...] = (
    {
        "name": "sexo_biologico",
        "label": "Sexo biologico",
        "type": "integer",
        "options": (("1", "Masculino"), ("2", "Feminino")),
    },
    {
        "name": "come_vegetaiis",
        "label": "Consumo de vegetais",
        "type": "integer",
        "options": (("1", "Raramente"), ("2", "As vezes"), ("3", "Sempre")),
    },
    {
        "name": "refeicoes_diariamente",
        "label": "Refeicoes diarias",
        "type": "integer",
        "options": (
            ("1", "Uma refeicao"),
            ("2", "Duas refeicoes"),
            ("3", "Tres refeicoes"),
            ("4", "Quatro refeicoes"),
            ("5", "Mais de quatro refeicoes"),
        ),
    },
    {
        "name": "come_entre_refeicao",
        "label": "Consumo entre refeicoes",
        "type": "string",
        "options": (
            ("no", "Nao consome"),
            ("somentimes", "As vezes"),
            ("frequently", "Frequentemente"),
            ("always", "Sempre"),
        ),
    },
    {
        "name": "litro_agua",
        "label": "Consumo diario de agua",
        "type": "integer",
        "options": (("1", "Ate 1 L"), ("2", "Entre 1-2 L"), ("3", "Mais de 2 L/dia")),
    },
    {
        "name": "frequencia_semanal_atvidade_fisica",
        "label": "Atividade fisica semanal",
        "type": "integer",
        "options": (
            ("0", "Nenhuma"),
            ("1", "1-2x na semana"),
            ("2", "3-4x na semana"),
            ("3", "5x na semana"),
            ("4", "Mais de 5x na semana"),
        ),
    },
    {
        "name": "horas_dispositivo_eletronico",
        "label": "Horas em dispositivo eletronico",
        "type": "integer",
        "options": (("0", "0-2h ao dia"), ("1", "3-5h ao dia"), ("2", "Mais de 5h ao dia")),
    },
    {
        "name": "consome_bebida_alcoolica",
        "label": "Consumo de bebida alcoolica",
        "type": "string",
        "options": (
            ("no", "Nao consome"),
            ("somentimes", "As vezes"),
            ("frequently", "Frequentemente"),
            ("always", "Sempre"),
        ),
    },
    {
        "name": "historico_familiar",
        "label": "Historico familiar",
        "type": "string",
        "options": (("yes", "Sim"), ("no", "Nao")),
    },
    {
        "name": "alimentos_calorico",
        "label": "Consumo de alimentos caloricos",
        "type": "string",
        "options": (("yes", "Sim"), ("no", "Nao")),
    },
    {
        "name": "meio_transporte",
        "label": "Meio de transporte",
        "type": "string",
        "options": (
            ("automobile", "Carro"),
            ("motorbike", "Moto"),
            ("bike", "Bicicleta"),
            ("public_transportation", "Transporte publico"),
            ("walking", "A pe"),
        ),
    },
    {
        "name": "obesity",
        "label": "Classificacao de obesidade",
        "type": "string",
        "required": False,
        "options": (
            ("Insufficient_Weight", "Abaixo do peso"),
            ("Normal_Weight", "Peso normal"),
            ("Overweight_Level_I", "Sobrepeso I"),
            ("Overweight_Level_II", "Sobrepeso II"),
            ("Obesity_Type_I", "Obesidade I"),
            ("Obesity_Type_II", "Obesidade II"),
            ("Obesity_Type_III", "Obesidade III"),
        ),
    },
)


def seed(database_url: str) -> None:
    engine = create_engine(database_url)
    with engine.begin() as connection:
        for field_order, field in enumerate(CATALOG, start=1):
            field_values = {
                "name": field["name"],
                "label": field["label"],
                "data_type": field["type"],
                "display_order": field_order,
                "required": field.get("required", True),
                "active": True,
            }
            field_insert = insert(DomainField.__table__).values(**field_values)
            field_id = connection.execute(
                field_insert.on_conflict_do_update(
                    constraint="uq_domain_field_name",
                    set_={**field_values, "updated_at": func.now()},
                ).returning(DomainField.id)
            ).scalar_one()
            for option_order, (value, label) in enumerate(field["options"], start=1):
                option_values = {
                    "domain_field_id": field_id,
                    "value": value,
                    "label": label,
                    "display_order": option_order,
                    "active": True,
                }
                option_insert = insert(DomainOption.__table__).values(**option_values)
                connection.execute(
                    option_insert.on_conflict_do_update(
                        constraint="uq_domain_option_field_value",
                        set_={**option_values, "updated_at": func.now()},
                    )
                )
    engine.dispose()


def main() -> None:
    database_url = os.getenv("DATABASE_URL")
    if database_url is None or not database_url.strip():
        raise RuntimeError("DATABASE_URL is required")
    seed(database_url)


if __name__ == "__main__":
    main()
