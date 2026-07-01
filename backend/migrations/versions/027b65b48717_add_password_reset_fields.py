"""add_password_reset_fields

Revision ID: 027b65b48717
Revises: 7cbf1708afd4
Create Date: 2026-06-28 16:28:30.874510
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "027b65b48717"
down_revision: Union[str, Sequence[str], None] = "7cbf1708afd4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("reset_code_hash", sa.String(), nullable=True),
    )

    op.add_column(
        "users",
        sa.Column("reset_code_expires_at", sa.DateTime(), nullable=True),
    )

    op.add_column(
        "users",
        sa.Column(
            "reset_attempts",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "users",
        sa.Column(
            "reset_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "reset_verified")
    op.drop_column("users", "reset_attempts")
    op.drop_column("users", "reset_code_expires_at")
    op.drop_column("users", "reset_code_hash")