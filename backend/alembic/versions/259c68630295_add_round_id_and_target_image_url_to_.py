"""add round_id and target_image_url to rounds

Revision ID: 259c68630295
Revises: 777e92f9a12c
Create Date: 2026-03-25 22:11:50.941020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '259c68630295'
down_revision: Union[str, Sequence[str], None] = '777e92f9a12c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("rounds", sa.Column("round_id", sa.String(), nullable=True))
    op.add_column("rounds", sa.Column("target_image_url", sa.String(), nullable=True))
    op.create_index(op.f("ix_rounds_round_id"), "rounds", ["round_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_rounds_round_id"), table_name="rounds")
    op.drop_column("rounds", "target_image_url")
    op.drop_column("rounds", "round_id")
