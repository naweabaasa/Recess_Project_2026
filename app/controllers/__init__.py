from app.controllers.auth_controller import auth_bp
from app.controllers.customer_auth_controller import customer_bp
from app.controllers.admin_controller import admin_bp
from app.controllers.category_controller import category_bp
from app.controllers.product_controller import product_bp
from app.controllers.cart_controller import cart_bp
from app.controllers.order_controller import order_bp
from app.controllers.payment_controller import payment_bp
from app.controllers.delivery_controller import delivery_bp
from app.controllers.public_controller import public_bp

all_blueprints = [
    auth_bp, customer_bp, admin_bp, category_bp, product_bp,
    cart_bp, order_bp, payment_bp, delivery_bp, public_bp,
]