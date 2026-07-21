from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Category
from app.utils.decorators import permission_required

category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")

@category_bp.route("", methods=["GET"])
@permission_required("manage_categories")
def list_categories():
    return jsonify([c.to_dict() for c in Category.query.all()]), 200

@category_bp.route("", methods=["POST"])
@permission_required("manage_categories")
def create_category():
    data = request.get_json() or {}
    category = Category(name=data.get("name"), description=data.get("description"),
                         status=data.get("status", "active"))
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201

@category_bp.route("/<int:category_id>", methods=["PUT"])
@permission_required("manage_categories")
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json() or {}
    category.name = data.get("name", category.name)
    category.description = data.get("description", category.description)
    category.status = data.get("status", category.status)
    db.session.commit()
    return jsonify(category.to_dict()), 200

@category_bp.route("/<int:category_id>", methods=["DELETE"])
@permission_required("manage_categories")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200