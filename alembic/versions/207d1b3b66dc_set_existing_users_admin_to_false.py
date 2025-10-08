"""Set existing users is_admin to False except first user

Revision ID: 207d1b3b66dc
Revises: add_is_admin_to_users
Create Date: 2025-07-24 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Boolean, Integer

# revision identifiers, used by Alembic.
revision = '207d1b3b66dc'
down_revision = 'add_is_admin_to_users'
branch_labels = None
depends_on = None

def upgrade():
    users = table('users',
                  column('id', Integer),
                  column('is_admin', Boolean))
    # Set all users is_admin to False except the one with lowest id (assumed first user)
    op.execute(
        users.update()
        .where(users.c.id !=
               sa.select(sa.func.min(users.c.id)).scalar_subquery())
        .values(is_admin=False)
    )

def downgrade():
    users = table('users',
                  column('id', Integer),
                  column('is_admin', Boolean))
    # Revert all users is_admin to True
    op.execute(
        users.update()
        .values(is_admin=True)
    )
