"""add streak columns to user_profiles

Revision ID: a3e7c81f9b22
Revises: 8f3c1a2b4d50
Create Date: 2026-04-30 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a3e7c81f9b22'
down_revision: Union[str, Sequence[str], None] = '8f3c1a2b4d50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user_profiles",
        sa.Column("current_streak", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "user_profiles",
        sa.Column("longest_streak", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "user_profiles",
        sa.Column("last_played_date", sa.Date(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("user_profiles", "last_played_date")
    op.drop_column("user_profiles", "longest_streak")
    op.drop_column("user_profiles", "current_streak")
