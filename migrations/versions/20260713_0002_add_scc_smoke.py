"""Add monitora_calorias (SCC) and fuma (SMOKE) columns to obesity_record."""

# ruff: noqa: E501

import sqlalchemy as sa
from alembic import op

revision = "20260713_0002"
down_revision = "20260703_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "obesity_record",
        sa.Column("monitora_calorias", sa.String(3), nullable=False, server_default="no"),
    )
    op.add_column(
        "obesity_record",
        sa.Column("fuma", sa.String(3), nullable=False, server_default="no"),
    )
    op.alter_column("obesity_record", "monitora_calorias", server_default=None)
    op.alter_column("obesity_record", "fuma", server_default=None)
    op.create_check_constraint(
        "ck_record_monitora_calorias", "obesity_record", "monitora_calorias IN ('yes', 'no')"
    )
    op.create_check_constraint("ck_record_fuma", "obesity_record", "fuma IN ('yes', 'no')")


def downgrade() -> None:
    op.drop_constraint("ck_record_fuma", "obesity_record", type_="check")
    op.drop_constraint("ck_record_monitora_calorias", "obesity_record", type_="check")
    op.drop_column("obesity_record", "fuma")
    op.drop_column("obesity_record", "monitora_calorias")
