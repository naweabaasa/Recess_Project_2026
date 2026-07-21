from app.extensions import db

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True)
    payment_method = db.Column(db.String(50))
    amount_paid = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default="pending")
    transaction_reference = db.Column(db.String(120))

    def to_dict(self):
        return {"id": self.id, "order_id": self.order_id, "payment_method": self.payment_method,
                "amount_paid": str(self.amount_paid), "status": self.status,
                "transaction_reference": self.transaction_reference}