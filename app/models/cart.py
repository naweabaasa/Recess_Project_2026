from app.extensions import db     # Imports the database instance

# Represents a customer's shopping cart and contains all the items they have added.
class ShoppingCart(db.Model):                                                            # Defines the ShoppingCart model.
    __tablename__ = "shopping_carts"                                                     # Database table name.
    id = db.Column(db.Integer, primary_key=True)                                         # Unique identifier for each shopping cart.
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), unique=True)      # Links the cart to a customer (one cart per customer).
    items = db.relationship("CartItem", backref="cart", cascade="all, delete-orphan")    # Creates a relationship with CartItem and deletes items when the cart is deleted.

    def __init__(self, customer_id=None):
        self.customer_id = customer_id

    # Converts the shopping cart object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "items": [i.to_dict() for i in self.items]
        }


# Represents an individual product in the shopping cart, including the selected product and its quantity.
class CartItem(db.Model):                                                  # Defines the CartItem model.
    __tablename__ = "cart_items"                                           # Database table name.
    id = db.Column(db.Integer, primary_key=True)                           # Unique identifier for each cart item.
    cart_id = db.Column(db.Integer, db.ForeignKey("shopping_carts.id"))    # Links the item to a shopping cart.
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))       # Links the item to a product.
    product = db.relationship("Product")                                   # Creates a relationship with the Product model.
    quantity = db.Column(db.Integer, default=1)                            # Stores the quantity of the product in the cart.

    def __init__(self, cart_id=None, product_id=None, quantity=1):
        self.cart_id = cart_id
        self.product_id = product_id
        self.quantity = quantity


    # Converts the cart item object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id,
            "product": self.product.to_dict() if self.product else None,
            "quantity": self.quantity
        }