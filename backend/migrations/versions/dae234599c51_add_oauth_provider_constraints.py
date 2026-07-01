"""add oauth provider constraints

Revision ID: dae234599c51
Revises: 7a8c7b268241
Create Date: 2026-06-30 16:39:58.426678

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dae234599c51"
down_revision: Union[str, Sequence[str], None] = "7a8c7b268241"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # make password nullable
    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(),
        nullable=True,
    )

    # drop index if it exists (safe reset)
    op.execute("DROP INDEX IF EXISTS ix_users_provider_id")

    # recreate correctly
    op.create_index(
        "ix_users_provider_id",
        "users",
        ["provider_id"],
        unique=True,
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_users_provider_id")

    op.alter_column(
        "users",
        "hashed_password",
        existing_type=sa.String(),
        nullable=False,
    )