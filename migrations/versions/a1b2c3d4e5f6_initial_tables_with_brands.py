"""initial tables with brands

Revision ID: a1b2c3d4e5f6
Revises: 
Create Date: 2026-08-05 12:41:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### Layer 0: Independent tables (no foreign keys) ###

    # 1. permissions
    op.create_table('permissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )

    # 2. roles
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    # 3. categories
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    # 4. brands
    op.create_table('brands',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('logo_url', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )

    # 5. customers
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone_number', sa.String(length=30), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )

    # ### Layer 1: Tables referencing Layer 0 ###

    # 6. role_permissions (references roles, permissions)
    op.create_table('role_permissions',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )

    # 7. admins (references roles)
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )

    # 8. orders (references customers)
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('order_date', sa.DateTime(), nullable=True),
    sa.Column('total_amount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('delivery_address', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # 9. shopping_carts (references customers)
    op.create_table('shopping_carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('customer_id')
    )

    # ### Layer 2: Tables referencing Layer 0 + Layer 1 ###

    # 10. products (references categories, brands, admins)
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admins.id'], ),
    sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # 11. cart_items (references shopping_carts, products)
    op.create_table('cart_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cart_id'], ['shopping_carts.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # 12. order_items (references orders, products)
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('sub_total', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # 13. payments (references orders)
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('payment_method', sa.String(length=50), nullable=True),
    sa.Column('amount_paid', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('transaction_reference', sa.String(length=120), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )

    # 14. deliveries (references orders)
    op.create_table('deliveries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('delivery_address', sa.String(length=255), nullable=True),
    sa.Column('delivery_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('delivery_fee', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### Drop in reverse dependency order ###
    op.drop_table('deliveries')
    op.drop_table('payments')
    op.drop_table('order_items')
    op.drop_table('cart_items')
    op.drop_table('products')
    op.drop_table('shopping_carts')
    op.drop_table('orders')
    op.drop_table('admins')
    op.drop_table('role_permissions')
    op.drop_table('customers')
    op.drop_table('brands')
    op.drop_table('categories')
    op.drop_table('roles')
    op.drop_table('permissions')
    # ### end Alembic commands ###
