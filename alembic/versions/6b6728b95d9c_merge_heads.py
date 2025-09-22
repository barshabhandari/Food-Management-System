"""merge heads

Revision ID: 6b6728b95d9c
Revises: 207d1b3b66dc, create_categories_table
Create Date: 2025-09-11 21:37:54.245856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b6728b95d9c'
down_revision: Union[str, Sequence[str], None] = ('207d1b3b66dc', 'create_categories_table')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
