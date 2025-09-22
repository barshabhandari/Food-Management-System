"""add is_admin to users

Revision ID: add_is_admin_to_users
Revises: dc343dbea5ab
Create Date: 2025-07-24 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_is_admin_to_users'
down_revision: Union[str, Sequence[str], None] = 'dc343dbea5ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), server_default=sa.text('False'), nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'is_admin')
