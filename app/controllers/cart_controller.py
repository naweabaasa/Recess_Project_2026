from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import ShoppingCart, CartItem

cart_bp = Blueprint("cart", __name__, url_prefix="/api/cart")

def get_cart():
    customer_id = get_jwt_identity()
    cart = ShoppingCart.query.filter_by(customer_id=customer_id).first()
    if not cart:
        cart = ShoppingCart(customer_id=customer_id)
        db.session.add(cart)
        db.session.commit()
    return cart

@cart_bp.route("", methods=["GET"])
@jwt_required()
def view_cart():
    return jsonify(get_cart().to_dict()), 200

@cart_bp.route("/items", methods=["POST"])
@jwt_required()
def add_item():
    cart = get_cart()
    data = request.get_json() or {}
    item = CartItem(cart_id=cart.id, product_id=data.get("product_id"),
                     quantity=data.get("quantity", 1))
    db.session.add(item)
    db.session.commit()
    return jsonify(cart.to_dict()), 200

@cart_bp.route("/items/<int:item_id>", methods=["PUT"])
@jwt_required()
def update_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    item.quantity = request.get_json().get("quantity", item.quantity)
    db.session.commit()
    return jsonify(get_cart().to_dict()), 200

@cart_bp.route("/items/<int:item_id>", methods=["DELETE"])
@jwt_required()
def remove_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify(get_cart().to_dict()), 200