"""add challenges table and attempts.challenge_id

Revision ID: 8f3c1a2b4d50
Revises: 71a50d844886
Create Date: 2026-04-20 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8f3c1a2b4d50"
down_revision: Union[str, Sequence[str], None] = "71a50d844886"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "challenges",
        sa.Column("id", sa.Uuid(), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("period_type", sa.String(), nullable=False),
        sa.Column("period_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("period_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("round_id", sa.String(), nullable=False),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default=sa.text("3")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_challenges_period_start"), "challenges", ["period_start"], unique=False)
    op.create_index(op.f("ix_challenges_period_type"), "challenges", ["period_type"], unique=False)

    op.add_column("attempts", sa.Column("challenge_id", sa.String(), nullable=True))
    op.create_index(op.f("ix_attempts_challenge_id"), "attempts", ["challenge_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_attempts_challenge_id"), table_name="attempts")
    op.drop_column("attempts", "challenge_id")
    op.drop_index(op.f("ix_challenges_period_type"), table_name="challenges")
    op.drop_index(op.f("ix_challenges_period_start"), table_name="challenges")
    op.drop_table("challenges")
