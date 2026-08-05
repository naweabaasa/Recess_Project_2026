# This controller manages product brands using CRUD operations
from flask import Blueprint, request, jsonify  # Import Flask tools
from app.extensions import db               # Import database connection
from app.models import Brand, Product       # Import Brand & Product database models


# Create Brand Blueprint
brand_bp = Blueprint("brands", __name__, url_prefix="/api/brands")


# Retrieves all brands.
# Accessible by admin/management or users with "manage_brands" or "manage_products" permission.
@brand_bp.route("", methods=["GET"])
def list_brands():
    brands = Brand.query.all()
    return jsonify([b.to_dict() for b in brands]), 200


# Retrieves a single brand by ID.
@brand_bp.route("/<int:brand_id>", methods=["GET"])
def get_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    return jsonify(brand.to_dict()), 200


# Creates a new product brand.
@brand_bp.route("", methods=["POST"])
def create_brand():
    data = request.get_json(silent=True) or {}      # Safely parse request JSON

    name = data.get("name")
    if not name or not name.strip():
        return jsonify({"error": "Brand name is required"}), 400

    name = name.strip()
    if Brand.query.filter_by(name=name).first():
        return jsonify({"error": "Brand with this name already exists"}), 400

    try:
        brand = Brand(
            name=name,
            description=data.get("description"),
            logo_url=data.get("logo_url"),
            status=data.get("status", "active")
        )

        db.session.add(brand)
        db.session.commit()
        return jsonify(brand.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create brand", "details": str(e)}), 500


# Updates an existing brand.
@brand_bp.route("/<int:brand_id>", methods=["PUT"])
def update_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)     # Find brand by ID or return 404

    data = request.get_json(silent=True) or {}   # Safely parse request JSON

    if "name" in data:
        new_name = data["name"].strip() if data["name"] else ""
        if not new_name:
            return jsonify({"error": "Brand name cannot be empty"}), 400
        existing = Brand.query.filter_by(name=new_name).first()
        if existing and existing.id != brand_id:
            return jsonify({"error": "Brand with this name already exists"}), 400
        brand.name = new_name

    if "description" in data:
        brand.description = data["description"]
    if "logo_url" in data:
        brand.logo_url = data["logo_url"]
    if "status" in data:
        brand.status = data["status"]

    try:
        db.session.commit()
        return jsonify(brand.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update brand", "details": str(e)}), 500


# Deletes a brand from the database.
@brand_bp.route("/<int:brand_id>", methods=["DELETE"])
def delete_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)     # Find brand by ID or return 404

    # Check if any products are associated with this brand
    associated_products = Product.query.filter_by(brand_id=brand_id).first()
    if associated_products:
        return jsonify({"error": "Cannot delete brand that is currently linked to products"}), 400

    try:
        db.session.delete(brand)
        db.session.commit()
        return jsonify({"message": "Brand deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete brand", "details": str(e)}), 500
