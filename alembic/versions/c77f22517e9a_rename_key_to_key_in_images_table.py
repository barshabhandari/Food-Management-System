"""rename Key to key in images table

Revision ID: c77f22517e9a
Revises: f12f8481a460
Create Date: 2025-07-19 21:44:13.745614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c77f22517e9a'
down_revision: Union[str, Sequence[str], None] = 'f12f8481a460'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("images", "Key", new_column_name="key")
    pass


def downgrade() -> None:
    op.alter_column("images", "key", new_column_name="Key")
    pass


