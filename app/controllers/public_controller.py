from flask import Blueprint, jsonify
# Blueprint creates routes,
# jsonify returns JSON responses.

from app.models import Category, Product, PageContent  # Import database models.


# Create Public Blueprint.
public_bp = Blueprint("public", __name__, url_prefix="/api/public")


# Displays all active categories.
@public_bp.route("/categories", methods=["GET"])
def categories():
    return jsonify([
        c.to_dict()
        for c in Category.query.filter_by(status="active").all()
    ]), 200


# Get only active products and return them
@public_bp.route("/products", methods=["GET"])
def products():
    return jsonify([p.to_dict() for p in Product.query.filter_by(status="active").all()]), 200


# Displays details of a specific product.
@public_bp.route("/products/<int:product_id>", methods=["GET"])
def product_detail(product_id):

    return jsonify(
        Product.query.get_or_404(product_id).to_dict()
    ), 200   # Find product by ID or return 404 if not found.

# Get page content for a specific public page (e.g. home, about)
@public_bp.route("/pages/<page_name>", methods=["GET"])
def get_page_content(page_name):
    contents = PageContent.query.filter_by(page_name=page_name).all()
    # Return as a dictionary mapping section keys to content
    result = {c.section_key: c.content for c in contents}
    return jsonify(result), 200

# This controller manages public access routes for customers.
# It allows anyone to view active product categories, active products, and details of a specific product without logging in.
# It uses the Category and Product models to retrieve information from the database.
