"""Add transaction_id column to payments table

Revision ID: add_transaction_id_to_payments
Revises: eead4ebac9b1
Create Date: 2025-10-06 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_transaction_id_to_payments'
down_revision = 'eead4ebac9b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('payments', sa.Column('transaction_id', sa.String(), nullable=True))


def downgrade():
    op.drop_column('payments', 'transaction_id')
