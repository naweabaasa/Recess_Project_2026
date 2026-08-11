"""remove_delivery_fee

Revision ID: 215858fe1e47
Revises: 91b9835eb93f
Create Date: 2026-08-11 14:58:40.231722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '215858fe1e47'
down_revision = '91b9835eb93f'
branch_labels = None
depends_on = None


def upgrade():
    # Remove delivery_fee column from deliveries table
    op.drop_column('deliveries', 'delivery_fee')


def downgrade():
    # Add back delivery_fee column if rollback is needed
    op.add_column('deliveries', sa.Column('delivery_fee', sa.Numeric(10, 2), nullable=True))
