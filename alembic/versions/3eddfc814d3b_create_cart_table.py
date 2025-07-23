"""create cart table

Revision ID: 3eddfc814d3b
Revises: c77f22517e9a
Create Date: 2025-07-23 14:34:03.913767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eddfc814d3b'
down_revision: Union[str, Sequence[str], None] = 'c77f22517e9a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("carts", sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
                    sa.Column("user_id", sa.Integer(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"),
                            nullable=False),
                    sa.Column("total_amount", sa.Float(), nullable=False))
    op.create_foreign_key("carts_user_fk", source_table="carts",referent_table="users",
                        local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_table("carts")
    pass
