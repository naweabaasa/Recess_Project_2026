from flask import Blueprint, request, jsonify
from app.extensions import db                           # Import database connection.
from app.models import Payment                          # Import Payment database model.


# Create Payment Blueprint.
payment_bp = Blueprint("payments", __name__, url_prefix="/api/payments")


# Retrieves all payment records.
# Requires "manage_payments" permission.
@payment_bp.route("", methods=["GET"])
def list_payments():

    # Return all payments as JSON.
    return jsonify([p.to_dict() for p in Payment.query.all()]), 200


# Creates a new payment record
@payment_bp.route("", methods=["POST"])
def create_payment():

    data = request.get_json() or {}            # Get payment data from request body.
    payment = Payment(                         # Create a new payment object.
        order_id=data.get("order_id"),
        payment_method=data.get("payment_method"),
        amount_paid=data.get("amount_paid"),
        status=data.get("status", "pending"),
        transaction_reference=data.get("transaction_reference")
    )

    db.session.add(payment)                  # Save payment information to database.
    db.session.commit()
    return jsonify(payment.to_dict()), 201   # Return created payment details.


# Updates the status of an existing payment.
@payment_bp.route("/<int:payment_id>", methods=["PUT"])
def update_payment(payment_id):

    payment = Payment.query.get_or_404(payment_id)         # Find payment by ID or return 404 if not found.
    payment.status = request.get_json().get(               # Update payment status.
        "status",
        payment.status
    )

    db.session.commit()                      # Save changes.
    return jsonify(payment.to_dict()), 200   # Return updated payment information.
