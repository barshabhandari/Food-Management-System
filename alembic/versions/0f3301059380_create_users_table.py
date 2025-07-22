"""create users table

Revision ID: 0f3301059380
Revises: fcf623aac367
Create Date: 2025-07-19 18:27:55.502934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f3301059380'
down_revision: Union[str, Sequence[str], None] = 'fcf623aac367'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer, primary_key=True, nullable=False),
                    sa.Column("email", sa.String, nullable=False, unique=True),
                    sa.Column("password", sa.String, nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone="True"), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column("is_active", sa.Boolean, server_default=sa.text('True'), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
