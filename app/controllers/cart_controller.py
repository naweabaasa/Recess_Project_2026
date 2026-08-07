# This controller manages the customer shopping cart system
from flask import Blueprint, request, jsonify
# Blueprint creates routes,
# request receives client data,
# jsonify returns JSON responses

from flask_jwt_extended import jwt_required, get_jwt_identity  # Import JWT functions

from sqlalchemy.exc import SQLAlchemyError  # Import database error type

from app.extensions import db  # Import database connection.

from app.models import ShoppingCart, CartItem  # Import shopping cart database models.


# Create Cart Blueprint.
cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")

# Function to get the logged-in customer's cart.
# If the customer does not have a cart, create a new one.
def get_cart(customer_id):
    cart = ShoppingCart.query.filter_by(customer_id=customer_id).first()  # Search for customer's existing cart.

    if not cart:    # Create a new cart if none exists.
        cart = ShoppingCart(customer_id=customer_id)
        db.session.add(cart)
        db.session.commit()
    return cart


# Displays the customer's shopping cart.
@cart_bp.route("", methods=["GET"])
@jwt_required()
def view_cart():
    customer_id = int(get_jwt_identity())  # Get logged-in customer ID
    return jsonify(get_cart(customer_id).to_dict()), 200


# Adds a product to the customer's cart.
@cart_bp.route("/items", methods=["POST"])
@jwt_required()
def add_item():
    customer_id = int(get_jwt_identity())  # Get logged-in customer ID
    cart = get_cart(customer_id)                   # Get customer's cart.
    data = request.get_json() or {}     # Get product information from request
    
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    
    # DUPLICATE FIX: Check if this product is already in the cart
    # CartItem.query.filter_by() searches for an item that matches these conditions
    existing_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()  # .first() returns the first match, or None if no match
    
    if existing_item:
        # Product already exists in cart, so just increase the quantity
        # Instead of creating a duplicate item, we update the existing one
        existing_item.quantity += quantity
        message = "Updated quantity in cart"
    else:
        # Product is not in cart yet, so create a new cart item
        item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(item)
        message = "Added to cart"
    
    # ERROR HANDLING: Wrap database commit in try-except
    try:
        db.session.commit()   # Save changes to database.
        
        # Return updated cart with a helpful message
        response_data = cart.to_dict()
        response_data["message"] = message
        return jsonify(response_data), 200
    
    except SQLAlchemyError as e:
        # Catch any database errors
        db.session.rollback()  # Undo changes
        return jsonify({
            "error": "Database error",
            "message": "Failed to add item to cart. Please try again."
        }), 500


# Updates the quantity of a cart item.
@cart_bp.route("/items/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    customer_id = int(get_jwt_identity())  # Get logged-in customer ID
    item = CartItem.query.get_or_404(item_id)    # Find cart item by ID or return 404.
    
    # SECURITY CHECK: Make sure this cart item belongs to the logged-in customer
    # We check by verifying the cart ownership
    if item.cart.customer_id != customer_id:
        # Return 403 Forbidden if this item doesn't belong to their cart
        return jsonify({"error": "You don't have permission to modify this cart item"}), 403
    
    item.quantity = request.get_json().get(
        "quantity",
        item.quantity
    )

    # ERROR HANDLING: Wrap database commit in try-except
    try:
        db.session.commit()    # Save changes.
        return jsonify(get_cart(customer_id).to_dict()), 200    # Return updated cart.
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": "Failed to update cart item. Please try again."
        }), 500


# Removes an item from the cart.
@cart_bp.route("/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def remove_item(item_id):
    customer_id = int(get_jwt_identity())  # Get logged-in customer ID
    # Find item by ID or return 404.
    item = CartItem.query.get_or_404(item_id)
    
    # SECURITY CHECK: Make sure this cart item belongs to the logged-in customer
    # We check by verifying the cart ownership
    if item.cart.customer_id != customer_id:
        # Return 403 Forbidden if this item doesn't belong to their cart
        return jsonify({"error": "You don't have permission to delete this cart item"}), 403

    # ERROR HANDLING: Wrap deletion in try-except
    try:
        db.session.delete(item)    # Delete item from database.
        db.session.commit()
        return jsonify(get_cart(customer_id).to_dict()), 200   # Return updated cart.
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": "Failed to remove item from cart. Please try again."
        }), 500
