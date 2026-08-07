# This controller manages the order process.
# It allows customers to checkout their cart, view their orders, and see order details.

from flask import Blueprint, request, jsonify  # Import Flask tools
# Blueprint creates routes,
# request receives client data,
# jsonify returns JSON responses.

from flask_jwt_extended import jwt_required, get_jwt_identity  # Import JWT functions

from app.extensions import db      # Import database connection.

from app.models import Order, OrderItem, ShoppingCart     # Import order-related database model
from app.utils.decorators import permission_required  # Import permission decorator


# Create Order Blueprint.
order_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


# Converts the customer's cart into an order.
@order_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout():
    customer_id = int(get_jwt_identity())  # Get logged-in customer ID from JWT token
    cart = ShoppingCart.query.filter_by(customer_id=customer_id).first()   # Find customer's shopping cart.

    if not cart or not cart.items:                        # Check if cart exists and has items.
        return jsonify({"error": "Cart is empty"}), 400

    data = request.get_json() or {}                         # Get checkout information.
    order = Order(                                           # Create a new order with customer details.
        customer_id=customer_id,
        delivery_address=data.get("delivery_address"),
        total_amount=0
    )

    db.session.add(order)                                # Add order to database.
    db.session.flush()                                   # Save order ID before creating order items.

    total = 0                                            # Calculate total order amount.

    for item in cart.items:                               # Move each cart item into the order.
        sub_total = item.product.price * item.quantity    # Calculate item subtotal.

        db.session.add(OrderItem(                         # Create order item record.
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.product.price,
            sub_total=sub_total
        ))

        total += sub_total                                # Add item price to total.

        db.session.delete(item)                           # Remove item from cart after checkout.

    order.total_amount = total                             # Update order total price.

    db.session.commit()                                    # Save all changes.
    return jsonify(order.to_dict(with_children=True)), 201   # Return completed order details.


# Displays all orders belonging to the logged-in customer.
@order_bp.route("", methods=["GET"])
@jwt_required()
def my_orders():
    customer_id = int(get_jwt_identity())  # Get logged-in customer ID from JWT token
    orders = Order.query.filter_by(                      # Get customer's orders from database.
        customer_id=customer_id
    ).all()
    return jsonify([o.to_dict() for o in orders]), 200    # Return orders list.


# Shows details of a specific order.
@order_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def order_detail(order_id):
    # SECURITY FIX: Get the logged-in customer's ID from JWT token
    customer_id = int(get_jwt_identity())
    
    order = Order.query.get_or_404(order_id)                  # Find order by ID or return 404.
    
    # IMPORTANT SECURITY CHECK: Make sure this order belongs to the logged-in customer
    # Without this check, any customer could view anyone else's orders!
    if order.customer_id != customer_id:
        # Return 403 Forbidden if the order doesn't belong to this customer
        return jsonify({"error": "You don't have permission to view this order"}), 403
    
    return jsonify(order.to_dict(with_children=True)), 200    # Return order details including items.


# Updates the status of an order.
# Only users with "manage_orders" permission can access.
@order_bp.route("/<int:order_id>/status", methods=["PUT"])
@permission_required("manage_orders")
def update_status(order_id):

    order = Order.query.get_or_404(order_id)                         # Find order by ID.
    order.status = request.get_json().get(                           # Update order status.
        "status",
        order.status
    )

    db.session.commit()                                              # Save changes.

    return jsonify(order.to_dict()), 200                             # Return updated order information.
