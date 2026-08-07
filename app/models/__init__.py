from app.models.admin import Admin, Role, Permission  # Imports the Admin, Role, and Permission models.

from app.models.category import Category  # Imports the Category model.

from app.models.brand import Brand  # Imports the Brand model.

from app.models.product import Product    # Imports the Product model.

from app.models.customer import Customer    # Imports the Customer model.

from app.models.cart import ShoppingCart, CartItem   # Imports the ShoppingCart and CartItem models.

from app.models.order import Order, OrderItem  # Imports the Order and OrderItem models.

from app.models.delivery import Delivery  # Imports the Delivery model


# This file imports all the database models into one place so they are available throughout the application 
# and can be detected by tools like Flask-Migrate when creating or updating database migrations.