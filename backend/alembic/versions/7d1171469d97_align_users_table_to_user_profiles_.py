"""align users table to user_profiles schema

Revision ID: 7d1171469d97
Revises: 259c68630295
Create Date: 2026-04-01 03:36:15.041551

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d1171469d97'
down_revision: Union[str, Sequence[str], None] = '259c68630295'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    if "users" not in tables:
        return

    op.rename_table("users", "user_profiles")

    op.alter_column("user_profiles", "username", new_column_name="display_name")

    op.add_column(
        "user_profiles",
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.execute(
        "UPDATE user_profiles SET last_seen_at = created_at WHERE last_seen_at IS NULL"
    )

    op.alter_column("user_profiles", "last_seen_at", nullable=False)

    op.drop_constraint("rounds_user_id_fkey", "rounds", type_="foreignkey")
    op.create_foreign_key(
        "rounds_user_id_fkey",
        "rounds",
        "user_profiles",
        ["user_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("rounds_user_id_fkey", "rounds", type_="foreignkey")
    op.create_foreign_key(
        "rounds_user_id_fkey",
        "rounds",
        "users",
        ["user_id"],
        ["id"],
    )

    op.drop_column("user_profiles", "last_seen_at")

    op.alter_column("user_profiles", "display_name", new_column_name="username")

    op.rename_table("user_profiles", "users")