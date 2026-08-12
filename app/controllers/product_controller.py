# This controller manages the product management system
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity  # Import function to get logged-in user's ID
from sqlalchemy.exc import IntegrityError, SQLAlchemyError  # Import database error types
from app.extensions import db                           # Import database connection.
from app.models import Product                          # Import Product database model.
from app.utils.decorators import permission_required    # Import permission decorator


# Create Product Blueprint.
product_bp = Blueprint("products", __name__, url_prefix="/api/products")

# Retrieves all products.
# Requires "manage_products" permission.
@product_bp.route("", methods=["GET"])
@permission_required("manage_products")
def list_products():

    # Return all products as JSON.
    return jsonify([p.to_dict() for p in Product.query.all()]), 200


# Creates a new product.
@product_bp.route("", methods=["POST"])
@permission_required("manage_products")
def create_product():
    
    # SECURITY FIX: Get the actual logged-in admin's ID from the JWT token
    # get_jwt_identity() returns the identity we stored when creating the token (admin.id)
    # We convert it to int because JWT stores it as a string
    admin_id = int(get_jwt_identity())

    data = request.get_json() or {}           # Get product data from request body.
    product = Product(                        # Create a new product object.
        name=data.get("name"),
        category_id=data.get("category_id"),
        image_url=data.get("image_url"),
        status=data.get("status", "draft"),
        admin_id=admin_id,  # Use the real admin ID from JWT token (audit trail!)
    )

    # ERROR HANDLING: Wrap database operations in try-except
    try:
        db.session.add(product)                    # Save product to database
        db.session.commit()
        return jsonify(product.to_dict()), 201     # Return created product details.
    
    except IntegrityError as e:
        # IntegrityError might happen if invalid foreign keys are used
        # For example: category_id that doesn't exist
        db.session.rollback()
        return jsonify({
            "error": "Database integrity error",
            "message": "Invalid category ID. Please check your input."
        }), 400
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": "Failed to create product. Please try again later."
        }), 500


# Updates an existing product.
@product_bp.route("/<int:product_id>", methods=["PUT"])
@permission_required("manage_products")
def update_product(product_id):

    product = Product.query.get_or_404(product_id)   # Find product by ID or return 404 if not found.

    data = request.get_json() or {}                  # Get updated product information.
    for field in [                                   # Update only fields provided in the request.
        "name",
        "category_id",
        "image_url",
        "status"
    ]:
        if field in data:
            setattr(product, field, data[field])

    # ERROR HANDLING: Wrap database commit in try-except
    try:
        db.session.commit()                          # Save changes.
        return jsonify(product.to_dict()), 200       # Return updated product.
    
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database integrity error",
            "message": "Invalid category ID. Please check your input."
        }), 400
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": "Failed to update product. Please try again later."
        }), 500


# Deletes a product from the database.
@product_bp.route("/<int:product_id>", methods=["DELETE"])
@permission_required("manage_products")
def delete_product(product_id):

    # Find product by ID or return 404.
    product = Product.query.get_or_404(product_id)

    # ERROR HANDLING: Wrap deletion in try-except
    try:
        # Remove product from database.
        db.session.delete(product)
        db.session.commit()

        # Return confirmation message.
        return jsonify({"message": "Product deleted successfully"}), 200
    
    except IntegrityError as e:
        # IntegrityError might happen if product is used in cart or orders
        db.session.rollback()
        return jsonify({
            "error": "Cannot delete product",
            "message": "This product is referenced in orders or carts. Remove those first."
        }), 400
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": "Failed to delete product. Please try again later."
        }), 500
