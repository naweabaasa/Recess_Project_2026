# Importing different Flask Blueprints from controller files.
# Each blueprint contains routes and logic for a specific part of the application.
from app.controllers.auth_controller import auth_bp               # Handles user authentication
from app.controllers.customer_auth_controller import customer_bp  # Handles customer-related actions
from app.controllers.admin_controller import admin_bp             # Handles admin operations
from app.controllers.category_controller import category_bp       # Handles product categories
from app.controllers.brand_controller import brand_bp           # Handles product brands
from app.controllers.product_controller import product_bp         # Handles product management
from app.controllers.cart_controller import cart_bp               # Handles shopping cart features
from app.controllers.order_controller import order_bp             # Handles order processing
from app.controllers.delivery_controller import delivery_bp       # Handles delivery management
from app.controllers.public_controller import public_bp           # Handles public pages/routes


# Store all application blueprints in one list.
# This makes it easier to register all routes in the main Flask application.
all_blueprints = [
    auth_bp, customer_bp, admin_bp, category_bp, brand_bp, product_bp,
    cart_bp, order_bp, delivery_bp, public_bp,
]
