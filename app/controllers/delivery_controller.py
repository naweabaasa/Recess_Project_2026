from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Delivery
from app.utils.decorators import permission_required

delivery_bp = Blueprint("deliveries", __name__, url_prefix="/api/deliveries")

@delivery_bp.route("", methods=["GET"])
@permission_required("manage_delivery")
def list_deliveries():
    return jsonify([d.to_dict() for d in Delivery.query.all()]), 200

@delivery_bp.route("", methods=["POST"])
@permission_required("manage_delivery")
def create_delivery():
    data = request.get_json() or {}
    delivery = Delivery(order_id=data.get("order_id"), delivery_address=data.get("delivery_address"),
                         delivery_fee=data.get("delivery_fee", 0), status=data.get("status", "pending"))
    db.session.add(delivery)
    db.session.commit()
    return jsonify(delivery.to_dict()), 201

@delivery_bp.route("/<int:delivery_id>", methods=["PUT"])
@permission_required("manage_delivery")
def update_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    data = request.get_json() or {}
    delivery.status = data.get("status", delivery.status)
    delivery.delivery_date = data.get("delivery_date", delivery.delivery_date)
    db.session.commit()
    return jsonify(delivery.to_dict()), 200