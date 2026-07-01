"""replace_reset_code_with_hash

Revision ID: 7a8c7b268241
Revises: 027b65b48717
Create Date: 2026-06-28 16:43:10.433005
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a8c7b268241"
down_revision: Union[str, Sequence[str], None] = "027b65b48717"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the new password-reset fields
    op.add_column(
        "users",
        sa.Column("reset_code_hash", sa.String(), nullable=True),
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

    # Remove the old plain-text reset code
    op.drop_column("users", "reset_code")

    # Remove temporary server defaults
    op.alter_column("users", "reset_attempts", server_default=None)
    op.alter_column("users", "reset_verified", server_default=None)


def downgrade() -> None:
    # Restore the old column
    op.add_column(
        "users",
        sa.Column("reset_code", sa.String(length=6), nullable=True),
    )

    # Remove the new fields
    op.drop_column("users", "reset_verified")
    op.drop_column("users", "reset_attempts")
    op.drop_column("users", "reset_code_hash")