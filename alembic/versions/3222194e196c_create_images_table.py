"""create images table

Revision ID: 3222194e196c
Revises: 0f3301059380
Create Date: 2025-07-19 18:29:33.734695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3222194e196c'
down_revision: Union[str, Sequence[str], None] = '0f3301059380'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("images",
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("Key", sa.String, nullable=False, unique=True)
                    )
    pass


def downgrade() -> None:
    op.drop_table("images")
    pass
