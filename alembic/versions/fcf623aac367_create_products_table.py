"""create products table

Revision ID: fcf623aac367
Revises: 
Create Date: 2025-07-19 18:23:41.094825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcf623aac367'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("products",sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("name", sa.String, nullable=False),
                    sa.Column("actual_price", sa.Integer, nullable=False),
                    sa.Column("discount_price", sa.Float, nullable=False),
                    sa.Column("stock", sa.Integer, nullable=False),
                    sa.Column("is_published", sa.Boolean, server_default=sa.text('True'), nullable=False),
                    # sa.Column("image_id", sa.Integer, sa.ForeignKey("images.id", ondelete="CASCADE"), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone="True"), server_default=sa.text('now()'),
                              nullable=False),
                    # sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table("products")
    pass
