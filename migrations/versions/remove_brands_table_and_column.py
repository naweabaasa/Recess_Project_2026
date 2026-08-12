"""remove brands table and column

Revision ID: remove_brands_001
Revises: 6972b34ea51d
Create Date: 2026-08-12 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'remove_brands_001'
down_revision = '6972b34ea51d'
branch_labels = None
depends_on = None


def upgrade():
    # First, drop the foreign key constraint if it exists
    # MySQL syntax to drop constraint
    op.execute('ALTER TABLE products DROP FOREIGN KEY IF EXISTS products_brand_id_fkey')
    op.execute('ALTER TABLE products DROP FOREIGN KEY IF EXISTS products_ibfk_2')
    
    # Remove the brand_id column from products table
    op.drop_column('products', 'brand_id')
    
    # Drop the brands table
    op.drop_table('brands')


def downgrade():
    # Recreate brands table
    op.create_table('brands',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('logo_url', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('admin_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['admin_id'], ['admins.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Add brand_id column back to products
    op.add_column('products', sa.Column('brand_id', sa.Integer(), nullable=True))
    op.create_foreign_key('products_brand_id_fkey', 'products', 'brands', ['brand_id'], ['id'])
