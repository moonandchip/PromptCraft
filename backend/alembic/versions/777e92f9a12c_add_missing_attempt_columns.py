"""add missing attempt columns

Revision ID: 777e92f9a12c
Revises: e0736feb8889
Create Date: 2026-03-25 19:03:18.507642

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "777e92f9a12c"
down_revision: Union[str, Sequence[str], None] = "e0736feb8889"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("attempts", sa.Column("round_id", sa.String(), nullable=True))
    op.add_column("attempts", sa.Column("generated_image_url", sa.String(), nullable=False, server_default=""))
    op.create_index(op.f("ix_attempts_round_id"), "attempts", ["round_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_attempts_round_id"), table_name="attempts")
    op.drop_column("attempts", "generated_image_url")
    op.drop_column("attempts", "round_id")