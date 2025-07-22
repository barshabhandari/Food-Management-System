"""add foreign_key to products table

Revision ID: f12f8481a460
Revises: 3222194e196c
Create Date: 2025-07-19 18:35:54.926030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f12f8481a460'
down_revision: Union[str, Sequence[str], None] = '3222194e196c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("image_id", sa.Integer(), nullable=True))
    op.add_column("products", sa.Column("owner_id", sa.Integer(), nullable=True))

    # Create foreign key constraints explicitly
    op.create_foreign_key("products_images_fk", source_table="products",
    referent_table= "images", local_cols=["image_id"], remote_cols=["id"],ondelete="CASCADE")
    op.create_foreign_key("products_owner_fk", source_table="products",
    referent_table= "users", local_cols=["owner_id"], remote_cols= ["id"],ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint("products_images_fk", table_name="products")
    op.drop_column("products", "image_id")
    op.drop_constraint("products_owner_fk", table_name="products")
    op.drop_column("products", "owner_id")
    pass
