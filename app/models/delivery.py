from app.extensions import db

class Delivery(db.Model):
    __tablename__ = "deliveries"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True)
    delivery_address = db.Column(db.String(255))
    delivery_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default="pending")
    delivery_fee = db.Column(db.Numeric(10, 2), default=0)

    def to_dict(self):
        return {"id": self.id, "order_id": self.order_id, "delivery_address": self.delivery_address,
                "status": self.status, "delivery_fee": str(self.delivery_fee)}