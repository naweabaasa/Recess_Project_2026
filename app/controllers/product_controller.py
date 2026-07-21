from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from app.models import Product
from app.utils.decorators import permission_required

product_bp = Blueprint("products", __name__, url_prefix="/api/products")

@product_bp.route("", methods=["GET"])
@permission_required("manage_products")
def list_products():
    return jsonify([p.to_dict() for p in Product.query.all()]), 200

@product_bp.route("", methods=["POST"])
@permission_required("manage_products")
def create_product():
    data = request.get_json() or {}
    product = Product(
        name=data.get("name"), category_id=data.get("category_id"),
        description=data.get("description"), price=data.get("price"),
        image_url=data.get("image_url"), status=data.get("status", "draft"),
        admin_id=get_jwt_identity(),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@product_bp.route("/<int:product_id>", methods=["PUT"])
@permission_required("manage_products")
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json() or {}
    for field in ["name", "category_id", "description", "price", "image_url", "status"]:
        if field in data:
            setattr(product, field, data[field])
    db.session.commit()
    return jsonify(product.to_dict()), 200

@product_bp.route("/<int:product_id>", methods=["DELETE"])
@permission_required("manage_products")
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200