from flask import Blueprint, jsonify
from app.models import Category, Product

public_bp = Blueprint("public", __name__, url_prefix="/api/public")

@public_bp.route("/categories", methods=["GET"])
def categories():
    return jsonify([c.to_dict() for c in Category.query.filter_by(status="active").all()]), 200

@public_bp.route("/products", methods=["GET"])
def products():
    return jsonify([p.to_dict() for p in Product.query.filter_by(status="active").all()]), 200

@public_bp.route("/products/<int:product_id>", methods=["GET"])
def product_detail(product_id):
    return jsonify(Product.query.get_or_404(product_id).to_dict()), 200