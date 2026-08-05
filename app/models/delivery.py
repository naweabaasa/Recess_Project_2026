from app.extensions import db    # Imports the database instance.

# Represents the delivery details for an order.
class Delivery(db.Model):                                                       # Defines the Delivery model.
    __tablename__ = "deliveries"                                                # Database table name.
    id = db.Column(db.Integer, primary_key=True)                                # Unique identifier for each delivery.
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True)   # Links the delivery to a specific order (one delivery per order).
    delivery_address = db.Column(db.String(255))                                # Stores the delivery address.
    delivery_date = db.Column(db.DateTime, nullable=True)                       # Stores the delivery date and time (optional).
    status = db.Column(db.String(20), default="pending")                        # Stores the delivery status (defaults to "pending").
    delivery_fee = db.Column(db.Numeric(10, 2), default=0)                      # Stores the delivery fee.

    def __init__(self, order_id=None, delivery_address=None, delivery_date=None, status="pending", delivery_fee=0):
        self.order_id = order_id
        self.delivery_address = delivery_address
        self.delivery_date = delivery_date
        self.status = status
        self.delivery_fee = delivery_fee

    # Converts the delivery object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id, 
            "order_id": self.order_id, 
            "delivery_address": self.delivery_address,
            "status": self.status, 
            "delivery_fee": str(self.delivery_fee)
            }