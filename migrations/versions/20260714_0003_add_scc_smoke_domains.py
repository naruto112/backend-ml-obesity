"""Add SCC and SMOKE fields to the domain catalog."""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import insert

revision = "20260714_0003"
down_revision = "20260713_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    domain_field = sa.table(
        "domain_field",
        sa.column("id", sa.BigInteger()),
        sa.column("name", sa.String()),
        sa.column("label", sa.String()),
        sa.column("data_type", sa.String()),
        sa.column("display_order", sa.SmallInteger()),
        sa.column("required", sa.Boolean()),
        sa.column("active", sa.Boolean()),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )
    domain_option = sa.table(
        "domain_option",
        sa.column("domain_field_id", sa.BigInteger()),
        sa.column("value", sa.String()),
        sa.column("label", sa.String()),
        sa.column("display_order", sa.SmallInteger()),
        sa.column("active", sa.Boolean()),
        sa.column("updated_at", sa.DateTime(timezone=True)),
    )
    connection = op.get_bind()

    connection.execute(
        sa.update(domain_field)
        .where(domain_field.c.name == "meio_transporte")
        .values(display_order=13)
    )
    connection.execute(
        sa.update(domain_field).where(domain_field.c.name == "obesity").values(display_order=14)
    )

    fields = (
        ("monitora_calorias", "Monitora calorias consumidas", 11),
        ("fuma", "Fumante", 12),
    )
    for name, label, display_order in fields:
        field_values = {
            "name": name,
            "label": label,
            "data_type": "string",
            "display_order": display_order,
            "required": True,
            "active": True,
        }
        field_id = connection.execute(
            insert(domain_field)
            .values(**field_values)
            .on_conflict_do_update(
                index_elements=[domain_field.c.name],
                set_={**field_values, "updated_at": sa.func.now()},
            )
            .returning(domain_field.c.id)
        ).scalar_one()

        for option_order, (value, option_label) in enumerate(
            (("yes", "Sim"), ("no", "Nao")), start=1
        ):
            option_values = {
                "domain_field_id": field_id,
                "value": value,
                "label": option_label,
                "display_order": option_order,
                "active": True,
            }
            connection.execute(
                insert(domain_option)
                .values(**option_values)
                .on_conflict_do_update(
                    index_elements=[domain_option.c.domain_field_id, domain_option.c.value],
                    set_={**option_values, "updated_at": sa.func.now()},
                )
            )


def downgrade() -> None:
    domain_field = sa.table(
        "domain_field",
        sa.column("id", sa.BigInteger()),
        sa.column("name", sa.String()),
        sa.column("display_order", sa.SmallInteger()),
    )
    domain_option = sa.table(
        "domain_option",
        sa.column("domain_field_id", sa.BigInteger()),
    )
    connection = op.get_bind()
    field_ids = sa.select(domain_field.c.id).where(
        domain_field.c.name.in_(("monitora_calorias", "fuma"))
    )

    connection.execute(
        sa.delete(domain_option).where(domain_option.c.domain_field_id.in_(field_ids))
    )
    connection.execute(
        sa.delete(domain_field).where(domain_field.c.name.in_(("monitora_calorias", "fuma")))
    )
    connection.execute(
        sa.update(domain_field)
        .where(domain_field.c.name == "meio_transporte")
        .values(display_order=11)
    )
    connection.execute(
        sa.update(domain_field).where(domain_field.c.name == "obesity").values(display_order=12)
    )
