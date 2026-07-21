from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Payment
from app.utils.decorators import permission_required

payment_bp = Blueprint("payments", __name__, url_prefix="/api/payments")

@payment_bp.route("", methods=["GET"])
@permission_required("manage_payments")
def list_payments():
    return jsonify([p.to_dict() for p in Payment.query.all()]), 200

@payment_bp.route("", methods=["POST"])
@permission_required("manage_payments")
def create_payment():
    data = request.get_json() or {}
    payment = Payment(order_id=data.get("order_id"), payment_method=data.get("payment_method"),
                       amount_paid=data.get("amount_paid"), status=data.get("status", "pending"),
                       transaction_reference=data.get("transaction_reference"))
    db.session.add(payment)
    db.session.commit()
    return jsonify(payment.to_dict()), 201

@payment_bp.route("/<int:payment_id>", methods=["PUT"])
@permission_required("manage_payments")
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    payment.status = request.get_json().get("status", payment.status)
    db.session.commit()
    return jsonify(payment.to_dict()), 200