from app.extensions import db   # Imports the database instance.
from datetime import datetime  # Imports the datetime module to record the order date.

# Represents a customer's order placed via the frontend form
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(120))
    customer_email = db.Column(db.String(120))
    customer_phone = db.Column(db.String(30))
    order_details = db.Column(db.Text)
    delivery_required = db.Column(db.Boolean, default=False)
    delivery_address = db.Column(db.String(255), nullable=True)
    inspiration_image = db.Column(db.String(500), nullable=True)  # Optional inspiration photo URL
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending")
    
    # Relationship to delivery (one-to-one)
    delivery = db.relationship('Delivery', backref='order', uselist=False, cascade='all, delete-orphan')

    def __init__(self, customer_name=None, customer_email=None, customer_phone=None, order_details=None, delivery_required=False, delivery_address=None, inspiration_image=None):
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_phone = customer_phone
        self.order_details = order_details
        self.delivery_required = delivery_required
        self.delivery_address = delivery_address
        self.inspiration_image = inspiration_image

    # Converts the order object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
            "customer_phone": self.customer_phone,
            "order_details": self.order_details,
            "delivery_required": self.delivery_required,
            "delivery_address": self.delivery_address,
            "inspiration_image": self.inspiration_image,
            "order_date": self.order_date.isoformat() if self.order_date else None,
            "status": self.status,
            "delivery_status": self.delivery.status if self.delivery else None
        }
