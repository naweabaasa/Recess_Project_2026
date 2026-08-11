# This controller manages the order process.
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Order, Delivery
from app.utils.decorators import permission_required

# Create Order Blueprint.
order_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

# Accepts a new order from the frontend form and saves it to the database.
# This route is public (no authentication required) since customers don't log in.
@order_bp.route("", methods=["POST"])
def create_order():
    data = request.get_json() or {}
    
    # Create a new order with the submitted details
    order = Order(
        customer_name=data.get("name"),
        customer_email=data.get("email"),
        customer_phone=data.get("phone"),
        order_details=data.get("orderDetails"),
        delivery_required=data.get("deliveryRequired", False),
        delivery_address=data.get("deliveryAddress")
    )

    try:
        db.session.add(order)
        db.session.flush()  # Flush to get the order.id before creating delivery
        
        # If delivery is required, automatically create a delivery record
        if order.delivery_required and order.delivery_address:
            delivery = Delivery(
                order_id=order.id,
                delivery_address=order.delivery_address,
                status="pending"
            )
            db.session.add(delivery)
        
        db.session.commit()
        return jsonify(order.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create order", "details": str(e)}), 500

# Displays all orders.
# Only users with "manage_orders" permission can access.
@order_bp.route("", methods=["GET"])
@permission_required("manage_orders")
def get_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders]), 200

# Updates the status of an order.
# Only users with "manage_orders" permission can access.
@order_bp.route("/<int:order_id>/status", methods=["PUT"])
@permission_required("manage_orders")
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.get_json().get("status", order.status)
    db.session.commit()
    return jsonify(order.to_dict()), 200

