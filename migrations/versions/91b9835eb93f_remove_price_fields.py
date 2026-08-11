"""remove_price_fields

Revision ID: 91b9835eb93f
Revises: a1b2c3d4e5f6
Create Date: 2026-08-11 09:34:33.441697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91b9835eb93f'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # Remove price field from products table
    op.drop_column('products', 'price')
    
    # Remove price-related fields from orders table
    op.drop_column('orders', 'total_amount')
    
    # Remove price-related fields from order_items table
    op.drop_column('order_items', 'unit_price')
    op.drop_column('order_items', 'sub_total')


def downgrade():
    # Add back price field to products table
    op.add_column('products', sa.Column('price', sa.Numeric(10, 2), nullable=True))
    
    # Add back price-related fields to orders table
    op.add_column('orders', sa.Column('total_amount', sa.Numeric(10, 2), nullable=True))
    
    # Add back price-related fields to order_items table
    op.add_column('order_items', sa.Column('unit_price', sa.Numeric(10, 2), nullable=True))
    op.add_column('order_items', sa.Column('sub_total', sa.Numeric(10, 2), nullable=True))
