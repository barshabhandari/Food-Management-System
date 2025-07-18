"""create users table

Revision ID: be10e5adb2f6
Revises: 2a89669d51f0
Create Date: 2025-07-15 11:51:48.750513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be10e5adb2f6'
down_revision: Union[str, Sequence[str], None] = '2a89669d51f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                        server_default=sa.text('now()'), nullable=False),
                        sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("email"))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
