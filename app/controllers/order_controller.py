from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Order, OrderItem, ShoppingCart
from app.utils.decorators import permission_required

order_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

@order_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    customer_id = get_jwt_identity()
    cart = ShoppingCart.query.filter_by(customer_id=customer_id).first()
    if not cart or not cart.items:
        return jsonify({"error": "Cart is empty"}), 400

    data = request.get_json() or {}
    order = Order(customer_id=customer_id, delivery_address=data.get("delivery_address"), total_amount=0)
    db.session.add(order)
    db.session.flush()

    total = 0
    for item in cart.items:
        sub_total = item.product.price * item.quantity
        db.session.add(OrderItem(order_id=order.id, product_id=item.product_id,
                                  quantity=item.quantity, unit_price=item.product.price,
                                  sub_total=sub_total))
        total += sub_total
        db.session.delete(item)

    order.total_amount = total
    db.session.commit()
    return jsonify(order.to_dict(with_children=True)), 201

@order_bp.route("", methods=["GET"])
@jwt_required()
def my_orders():
    orders = Order.query.filter_by(customer_id=get_jwt_identity()).all()
    return jsonify([o.to_dict() for o in orders]), 200

@order_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict(with_children=True)), 200

@order_bp.route("/<int:order_id>/status", methods=["PUT"])
@permission_required("manage_orders")
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.get_json().get("status", order.status)
    db.session.commit()
    return jsonify(order.to_dict()), 200