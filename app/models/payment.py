from app.extensions import db  # Imports the database instance.

class Payment(db.Model):                                                           # Defines the Payment model.
    __tablename__ = "payments"                                                     # Database table name.
    id = db.Column(db.Integer, primary_key=True)                                   # Unique identifier for each payment.
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True)      # Links the payment to a specific order (one payment per order).
    payment_method = db.Column(db.String(50))                                      # Stores the payment method (e.g., Cash, Credit Card, Mobile Money).
    amount_paid = db.Column(db.Numeric(10, 2))                                     # Stores the amount paid.
    status = db.Column(db.String(20), default="pending")                           # Stores the payment status (defaults to "pending").
    transaction_reference = db.Column(db.String(120))                              # Stores the payment transaction reference number.

    # Converts the payment object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id, 
            "order_id": self.order_id, 
            "payment_method": self.payment_method,
            "amount_paid": str(self.amount_paid), 
            "status": self.status,
            "transaction_reference": self.transaction_reference
            }