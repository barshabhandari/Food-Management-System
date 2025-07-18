"""Create product table

Revision ID: 2a89669d51f0
Revises: 
Create Date: 2025-07-14 22:46:09.190031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a89669d51f0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("products",sa.Column("id", sa.Integer(),nullable=False),
                    sa.Column("name", sa.String(), nullable=False),
                    sa.Column("actual_price", sa.Integer(), nullable=False),
                    sa.Column("discount_price", sa.Float(), nullable=False),
                    sa.Column("stock", sa.Integer(), nullable=False),
                    sa.Column("is_published", sa.Boolean(), server_default="True", nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone="True"),
                              server_default=sa.text('now()'), nullable=False),
                              sa.PrimaryKeyConstraint("id"))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
