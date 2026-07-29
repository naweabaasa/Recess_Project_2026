# This controller manages product categories using CRUD operations 
from flask import Blueprint, request, jsonify  # Import Flask tools
# Blueprint creates a group of routes,
# request receives data from the client,
# jsonify returns JSON responses.

from app.extensions import db               # Import database connection.

from app.models import Category          # Import Category database model.

from app.utils.decorators import permission_required   # Import permission checking decorator.


# Create Category Blueprint.
category_bp = Blueprint("categories", __name__, url_prefix="/api/categories")



# Retrieves all categories.
# Only users with "manage_categories" permission can access.
@category_bp.route("", methods=["GET"])
@permission_required("manage_categories")
def list_categories():
    return jsonify([c.to_dict() for c in Category.query.all()]), 200



# Creates a new product category.
@category_bp.route("", methods=["POST"])
@permission_required("manage_categories")
def create_category():

    data = request.get_json() or {}              # Get category data from request body.
    category = Category(                         # Create a new category object.
        name=data.get("name"), 
        description=data.get("description"),
        status=data.get("status", "active")
    )

    # Save category to database.
    db.session.add(category)
    db.session.commit()

    # Return created category details.
    return jsonify(category.to_dict()), 201



# Updates an existing category.
@category_bp.route("/<int:category_id>", methods=["PUT"])
@permission_required("manage_categories")
def update_category(category_id):

   
    category = Category.query.get_or_404(category_id)     # Find category by ID or return 404 if not found.

    data = request.get_json() or {}                       # Get updated information.
    # Update category fields.
    category.name = data.get("name", category.name)
    category.description = data.get("description", category.description)
    category.status = data.get("status", category.status)

    db.session.commit()    # Save changes.
    return jsonify(category.to_dict()), 200



# Deletes a category from the database.
@category_bp.route("/<int:category_id>", methods=["DELETE"])
@permission_required("manage_categories")
def delete_category(category_id):

    category = Category.query.get_or_404(category_id)        # Find category by ID or return 404.

    db.session.delete(category)                              # Remove category from database.
    db.session.commit()

    return jsonify({"message": "Category deleted"}), 200      # Return deletion confirmation message.