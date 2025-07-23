"""Rename column in table

Revision ID: b27fa98c876f
Revises: 3eddfc814d3b
Create Date: 2025-07-23 15:44:50.785189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b27fa98c876f'
down_revision: Union[str, Sequence[str], None] = '3eddfc814d3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("carts", "user_id", new_column_name="owner_id",)
    pass


def downgrade() -> None:
    op.alert_column("carts", "owner_id", new_column_name="user_id")
    pass
