from app.extensions import db   # Imports the database instance.

from datetime import datetime  # Imports the datetime module to record the order date.

# Represents a customer's order
class Order(db.Model):                                                  # Defines the Order model.
    __tablename__ = "orders"                                            # Database table name.
    id = db.Column(db.Integer, primary_key=True)                        # Unique identifier for each order.
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))  # Links the order to a customer.
    order_date = db.Column(db.DateTime, default=datetime.utcnow)        # Stores the date and time the order was created.
    total_amount = db.Column(db.Numeric(10, 2), default=0)              # Stores the total cost of the order.
    status = db.Column(db.String(20), default="pending")                # Stores the current order status (defaults to "pending").
    delivery_address = db.Column(db.String(255))                        # Stores the delivery address for the order.
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")   # Creates a relationship with all items in the order.
    payment = db.relationship("Payment", backref="order", uselist=False)                  # Creates a one-to-one relationship with the payment.
    delivery = db.relationship("Delivery", backref="order", uselist=False)                # Creates a one-to-one relationship with the delivery.


    #Converts the order object into a dictionary.
    def to_dict(self, with_children=False):
        data = {"id": self.id, "customer_id": self.customer_id,
                "total_amount": str(self.total_amount), "status": self.status,
                "delivery_address": self.delivery_address}
        
        # Includes related items, payment, and delivery details if requested.
        if with_children:    
            data["items"] = [i.to_dict() for i in self.items]
            data["payment"] = self.payment.to_dict() if self.payment else None
            data["delivery"] = self.delivery.to_dict() if self.delivery else None
        return data   # Returns the order data.



# Represents an individual product within an order,
class OrderItem(db.Model):                                             # Database table name.
    __tablename__ = "order_items"                                      # Unique identifier for each order item.
    id = db.Column(db.Integer, primary_key=True)                       # Links the item to an order.
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))       # Links the item to an order.
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))   # Links the item to a product.
    product = db.relationship("Product")                               # Creates a relationship with the Product model.
    quantity = db.Column(db.Integer)                                   # Stores the quantity of the product ordered.
    unit_price = db.Column(db.Numeric(10, 2))                          # Stores the price of one unit of the product.
    sub_total = db.Column(db.Numeric(10, 2))                           # Stores the total cost for this item (quantity × unit price).

    # Converts the order item object into a dictionary.
    def to_dict(self):
        return {"id": self.id, 
                "product_id": self.product_id,
                "quantity": self.quantity, 
                "unit_price": str(self.unit_price),
                "sub_total": str(self.sub_total)
                }