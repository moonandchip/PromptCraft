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
    # These columns are already created by the initial migration (e0736feb8889).
    # This migration existed to backfill them on an older RDS schema and is now a no-op.
    pass


def downgrade() -> None:
    pass
