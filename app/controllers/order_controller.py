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
        delivery_address=data.get("deliveryAddress"),
        inspiration_image=data.get("inspirationImage")  # Optional inspiration photo URL
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

# Batch imports orders from JSON list
@order_bp.route("/import", methods=["POST"])
@permission_required("manage_orders")
def import_orders():
    data = request.get_json() or {}
    items = data.get("orders", [])
    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "No orders provided for import"}), 400

    imported_count = 0
    for idx, item in enumerate(items):
        name = item.get("customer_name") or item.get("name")
        if not name:
            continue
        order = Order(
            customer_name=name,
            customer_email=item.get("customer_email") or item.get("email") or "",
            customer_phone=item.get("customer_phone") or item.get("phone") or "",
            order_details=item.get("order_details") or item.get("orderDetails") or "Imported order",
            delivery_required=bool(item.get("delivery_required") or item.get("deliveryRequired")),
            delivery_address=item.get("delivery_address") or item.get("deliveryAddress") or "",
            inspiration_image=item.get("inspiration_image") or None
        )
        if "status" in item and item["status"]:
            order.status = item["status"]
        db.session.add(order)
        db.session.flush()

        if order.delivery_required and order.delivery_address:
            delivery = Delivery(
                order_id=order.id,
                delivery_address=order.delivery_address,
                status=item.get("delivery_status") or "pending"
            )
            db.session.add(delivery)
        imported_count += 1

    try:
        db.session.commit()
        return jsonify({
            "message": f"Successfully imported {imported_count} orders",
            "imported_count": imported_count
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to import orders", "details": str(e)}), 500

# Displays all orders.
# Only users with "manage_orders" permission can access.
@order_bp.route("", methods=["GET"])
@permission_required("manage_orders")
def get_orders():
    orders = Order.query.order_by(Order.id.desc()).all()
    return jsonify([o.to_dict() for o in orders]), 200

# Get single order details
@order_bp.route("/<int:order_id>", methods=["GET"])
@permission_required("manage_orders")
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict()), 200

# Updates full order details
@order_bp.route("/<int:order_id>", methods=["PUT"])
@permission_required("manage_orders")
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json() or {}

    if "customer_name" in data:
        order.customer_name = data["customer_name"]
    if "customer_email" in data:
        order.customer_email = data["customer_email"]
    if "customer_phone" in data:
        order.customer_phone = data["customer_phone"]
    if "order_details" in data:
        order.order_details = data["order_details"]
    if "status" in data:
        order.status = data["status"]
    if "delivery_address" in data:
        order.delivery_address = data["delivery_address"]
    if "delivery_required" in data:
        order.delivery_required = bool(data["delivery_required"])

    # Synchronize with delivery record
    if order.delivery_required:
        if order.delivery:
            if order.delivery_address:
                order.delivery.delivery_address = order.delivery_address
        else:
            delivery = Delivery(
                order_id=order.id,
                delivery_address=order.delivery_address or "",
                status="pending"
            )
            db.session.add(delivery)
    elif order.delivery:
        db.session.delete(order.delivery)

    try:
        db.session.commit()
        return jsonify(order.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update order", "details": str(e)}), 500

# Updates the status of an order.
# Only users with "manage_orders" permission can access.
@order_bp.route("/<int:order_id>/status", methods=["PUT"])
@permission_required("manage_orders")
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.get_json().get("status", order.status)
    db.session.commit()
    return jsonify(order.to_dict()), 200

# Deletes an order from the database.
@order_bp.route("/<int:order_id>", methods=["DELETE"])
@permission_required("manage_orders")
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete order", "details": str(e)}), 500

