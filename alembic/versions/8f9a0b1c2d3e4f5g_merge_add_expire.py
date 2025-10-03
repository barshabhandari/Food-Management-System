"""merge add expire

Revision ID: 8f9a0b1c2d3e4f5g
Revises: 6b6728b95d9c, dc343dbea5ab
Create Date: 2025-10-03 11:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f9a0b1c2d3e4f5g'
down_revision: Union[str, Sequence[str], None] = ('6b6728b95d9c', 'dc343dbea5ab')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
