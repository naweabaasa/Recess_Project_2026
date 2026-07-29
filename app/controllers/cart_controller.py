# This controller manages the customer shopping cart system
from flask import Blueprint, request, jsonify
# Blueprint creates routes,
# request receives client data,
# jsonify returns JSON responses

from flask_jwt_extended import jwt_required, get_jwt_identity # Imports JWT functions:
# jwt_required protects routes,
# get_jwt_identity gets the logged-in user's ID

from app.extensions import db  # Import database connection.

from app.models import ShoppingCart, CartItem # Import shopping cart database models.


# Create Cart Blueprint.
cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")  

# Function to get the logged-in customer's cart.
# If the customer does not have a cart, create a new one.
def get_cart():

    customer_id = get_jwt_identity()                                      # Get customer ID from JWT token.
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
    return jsonify(get_cart().to_dict()), 200



# Adds a product to the customer's cart.
@cart_bp.route("/items", methods=["POST"])
@jwt_required()
def add_item():

    cart = get_cart()                   # Get customer's cart.
    data = request.get_json() or {}     # Get product information from request

     # Create a new cart item.
    item = CartItem(                   
        cart_id=cart.id, 
        product_id=data.get("product_id"),
        quantity=data.get("quantity", 1))
    
    db.session.add(item)
    db.session.commit()   # Save item to database. 

    return jsonify(cart.to_dict()), 200  # Return updated cart.



# Updates the quantity of a cart item.
@cart_bp.route("/items/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
   
    item = CartItem.query.get_or_404(item_id)    # Find cart item by ID or return 404.
    item.quantity = request.get_json().get(
        "quantity", 
        item.quantity
    )   

    db.session.commit()    # Save changes.
    return jsonify(get_cart().to_dict()), 200    # Return updated cart.



# Removes an item from the cart.
@cart_bp.route("/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def remove_item(item_id):

    # Find item by ID or return 404.
    item = CartItem.query.get_or_404(item_id)

    db.session.delete(item)    # Delete item from database.  
    db.session.commit()   
    return jsonify(get_cart().to_dict()), 200   # Return updated cart.