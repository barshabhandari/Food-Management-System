"""add manufacture_date to products table

Revision ID: d24a546353a9
Revises: add_transaction_id_to_payments
Create Date: 2025-10-20 21:31:17.437374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd24a546353a9'
down_revision: Union[str, Sequence[str], None] = 'add_transaction_id_to_payments'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('manufacture_date', sa.Date(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'manufacture_date')
