"""Update images

Revision ID: 94e4095dc575
Revises: 4247f6972ee7
Create Date: 2025-07-18 13:17:35.847150
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import TIMESTAMP, Boolean, Column, Float, ForeignKey, Integer, String, text

# revision identifiers, used by Alembic.
revision: str = '94e4095dc575'
down_revision: Union[str, Sequence[str], None] = '4247f6972ee7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # Create 'images' table
    op.create_table(
        'images',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('key', sa.String, unique=True, nullable=False)
    )

    # Add 'image_id' column to 'products' table
    op.add_column('products', sa.Column('image_id', sa.Integer, sa.ForeignKey('images.id', ondelete="CASCADE"), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    # Drop 'image_id' column from 'products' table
    op.drop_column('products', 'image_id')
    
    # Drop 'images' table
    op.drop_table('images')
