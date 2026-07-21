from datetime import datetime
from app.extensions import db

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.String(20), default="pending")
    delivery_address = db.Column(db.String(255))

    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")
    payment = db.relationship("Payment", backref="order", uselist=False)
    delivery = db.relationship("Delivery", backref="order", uselist=False)

    def to_dict(self, with_children=False):
        data = {"id": self.id, "customer_id": self.customer_id,
                "total_amount": str(self.total_amount), "status": self.status,
                "delivery_address": self.delivery_address}
        if with_children:
            data["items"] = [i.to_dict() for i in self.items]
            data["payment"] = self.payment.to_dict() if self.payment else None
            data["delivery"] = self.delivery.to_dict() if self.delivery else None
        return data

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product = db.relationship("Product")
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric(10, 2))
    sub_total = db.Column(db.Numeric(10, 2))

    def to_dict(self):
        return {"id": self.id, "product_id": self.product_id,
                "quantity": self.quantity, "unit_price": str(self.unit_price),
                "sub_total": str(self.sub_total)}