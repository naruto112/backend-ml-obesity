"""Create the domain catalog and obesity record tables."""

# ruff: noqa: E501

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "20260703_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "domain_field",
        sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("label", sa.String(128), nullable=False),
        sa.Column("data_type", sa.String(16), nullable=False),
        sa.Column("display_order", sa.SmallInteger(), nullable=False),
        sa.Column("required", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("data_type IN ('integer', 'string')", name="ck_domain_field_data_type"),
        sa.PrimaryKeyConstraint("id", name="pk_domain_field"),
        sa.UniqueConstraint("name", name="uq_domain_field_name"),
    )
    op.create_table(
        "domain_option",
        sa.Column("id", sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column("domain_field_id", sa.BigInteger(), nullable=False),
        sa.Column("value", sa.String(64), nullable=False),
        sa.Column("label", sa.String(128), nullable=False),
        sa.Column("display_order", sa.SmallInteger(), nullable=False),
        sa.Column("active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["domain_field_id"], ["domain_field.id"], name="fk_domain_option_domain_field"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_domain_option"),
        sa.UniqueConstraint("domain_field_id", "value", name="uq_domain_option_field_value"),
    )
    op.create_index(
        "ix_domain_option_field_active_order",
        "domain_option",
        ["domain_field_id", "active", "display_order"],
    )
    op.create_table(
        "obesity_record",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("idade", sa.SmallInteger(), nullable=False),
        sa.Column("sexo_biologico", sa.SmallInteger(), nullable=False),
        sa.Column("come_vegetaiis", sa.SmallInteger(), nullable=False),
        sa.Column("refeicoes_diariamente", sa.SmallInteger(), nullable=False),
        sa.Column("come_entre_refeicao", sa.String(16), nullable=False),
        sa.Column("litro_agua", sa.SmallInteger(), nullable=False),
        sa.Column("frequencia_semanal_atvidade_fisica", sa.SmallInteger(), nullable=False),
        sa.Column("horas_dispositivo_eletronico", sa.SmallInteger(), nullable=False),
        sa.Column("consome_bebida_alcoolica", sa.String(16), nullable=False),
        sa.Column("historico_familiar", sa.String(3), nullable=False),
        sa.Column("alimentos_calorico", sa.String(3), nullable=False),
        sa.Column("meio_transporte", sa.String(32), nullable=False),
        sa.Column("obesity", sa.String(32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("idade BETWEEN 1 AND 120", name="ck_record_idade"),
        sa.CheckConstraint("sexo_biologico IN (1, 2)", name="ck_record_sexo"),
        sa.CheckConstraint("come_vegetaiis IN (1, 2, 3)", name="ck_record_vegetais"),
        sa.CheckConstraint("refeicoes_diariamente IN (1, 2, 3, 4, 5)", name="ck_record_refeicoes"),
        sa.CheckConstraint(
            "come_entre_refeicao IN ('no', 'somentimes', 'frequently', 'always')",
            name="ck_record_entre_refeicao",
        ),
        sa.CheckConstraint("litro_agua IN (1, 2, 3)", name="ck_record_agua"),
        sa.CheckConstraint(
            "frequencia_semanal_atvidade_fisica IN (0, 1, 2, 3, 4)", name="ck_record_atividade"
        ),
        sa.CheckConstraint(
            "horas_dispositivo_eletronico IN (0, 1, 2)", name="ck_record_dispositivo"
        ),
        sa.CheckConstraint(
            "consome_bebida_alcoolica IN ('no', 'somentimes', 'frequently', 'always')",
            name="ck_record_alcool",
        ),
        sa.CheckConstraint("historico_familiar IN ('yes', 'no')", name="ck_record_historico"),
        sa.CheckConstraint("alimentos_calorico IN ('yes', 'no')", name="ck_record_calorico"),
        sa.CheckConstraint(
            "meio_transporte IN ('automobile', 'motorbike', 'bike', 'public_transportation', 'walking')",
            name="ck_record_transporte",
        ),
        sa.CheckConstraint(
            "obesity IN ('Insufficient_Weight', 'Normal_Weight', 'Overweight_Level_I', 'Overweight_Level_II', 'Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III')",
            name="ck_record_obesity",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_obesity_record"),
    )
    op.create_index("ix_obesity_record_created_at", "obesity_record", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_obesity_record_created_at", table_name="obesity_record")
    op.drop_table("obesity_record")
    op.drop_index("ix_domain_option_field_active_order", table_name="domain_option")
    op.drop_table("domain_option")
    op.drop_table("domain_field")
