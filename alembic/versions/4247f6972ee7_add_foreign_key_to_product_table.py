"""add foreign_key to product table

Revision ID: 4247f6972ee7
Revises: be10e5adb2f6
Create Date: 2025-07-15 17:18:20.998440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4247f6972ee7'
down_revision: Union[str, Sequence[str], None] = 'be10e5adb2f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key('product_user_fk', source_table='products', referent_table="users",
                        local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('product_user_fk', table_name='products')
    op.drop_column('products', 'owner_id')
    pass
