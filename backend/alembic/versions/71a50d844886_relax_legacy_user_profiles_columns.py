"""relax legacy user_profiles columns

Revision ID: 71a50d844886
Revises: 7d1171469d97
Create Date: 2026-04-01 03:51:20.775616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71a50d844886'
down_revision: Union[str, Sequence[str], None] = '7d1171469d97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("user_profiles")}

    if "password_hash" in columns:
        op.alter_column("user_profiles", "password_hash", existing_type=sa.String(), nullable=True)
    if "total_score" in columns:
        op.alter_column("user_profiles", "total_score", existing_type=sa.Integer(), nullable=True)
    if "role" in columns:
        op.alter_column("user_profiles", "role", existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    op.alter_column("user_profiles", "role", existing_type=sa.String(), nullable=False)
    op.alter_column("user_profiles", "total_score", existing_type=sa.Integer(), nullable=False)
    op.alter_column("user_profiles", "password_hash", existing_type=sa.String(), nullable=False)