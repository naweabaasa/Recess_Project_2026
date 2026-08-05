# This controller manages the product management system
from flask import Blueprint, request, jsonify
from app.extensions import db                           # Import database connection.
from app.models import Product                          # Import Product database model.


# Create Product Blueprint.
product_bp = Blueprint("products", __name__, url_prefix="/api/products")

# Retrieves all products.
# Requires "manage_products" permission.


@product_bp.route("", methods=["GET"])
def list_products():

    # Return all products as JSON.
    return jsonify([p.to_dict() for p in Product.query.all()]), 200


# Creates a new product.
@product_bp.route("", methods=["POST"])
def create_product():

    data = request.get_json() or {}           # Get product data from request body.
    product = Product(                        # Create a new product object.
        name=data.get("name"),
        category_id=data.get("category_id"),
        brand_id=data.get("brand_id"),
        description=data.get("description"),
        price=data.get("price"),
        image_url=data.get("image_url"),
        status=data.get("status", "draft"),
        admin_id=1,  # Default admin ID (no authentication).
    )

    db.session.add(product)                    # Save product to database
    db.session.commit()
    return jsonify(product.to_dict()), 201     # Return created product details.


# Updates an existing product.
@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):

    product = Product.query.get_or_404(product_id)   # Find product by ID or return 404 if not found.

    data = request.get_json() or {}                  # Get updated product information.
    for field in [                                   # Update only fields provided in the request.
        "name",
        "category_id",
        "brand_id",
        "description",
        "price",
        "image_url",
        "status"
    ]:
        if field in data:
            setattr(product, field, data[field])

    db.session.commit()                          # Save changes.
    return jsonify(product.to_dict()), 200       # Return updated product.


# Deletes a product from the database.
@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    # Find product by ID or return 404.
    product = Product.query.get_or_404(product_id)

    # Remove product from database.
    db.session.delete(product)
    db.session.commit()

    # Return confirmation message.
    return jsonify({"message": "Product deleted"}), 200
