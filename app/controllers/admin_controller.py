# This controller manages admin CRUD operations

from flask import Blueprint, request, jsonify
# Blueprint creates a group of related routes,
# request gets data sent by the client,
# jsonify returns JSON responses.

from sqlalchemy.exc import IntegrityError, SQLAlchemyError  # Import database error types

from app.extensions import db  # Import database connection.

from app.models import Admin, Role  # Import Admin model and Role model from the database.

from app.utils.decorators import permission_required  # Import permission decorator.




# Creating an Admin Blueprint.
admin_bp = Blueprint("admins", __name__, url_prefix="/api/admins")


# Returns a list of all admins.
# Only users with "manage_admins" permission can access.
@admin_bp.route("", methods=["GET"])
@permission_required("manage_admins")
def list_admins():
    return jsonify([a.to_dict() for a in Admin.query.all()]), 200


# Creates a new admin account.
# Receives admin details from the request body.
@admin_bp.route("", methods=["POST"])
@permission_required("manage_admins")
def create_admin():

    data = request.get_json() or {}                        # Get JSON data from client
    
    # INPUT VALIDATION: Check if required fields are provided
    # Without validation, we could create incomplete admin records
    
    # Check if full_name is provided and not empty
    if not data.get("full_name") or not data.get("full_name").strip():
        return jsonify({"error": "Full name is required"}), 400
    
    # Check if email is provided and not empty
    if not data.get("email") or not data.get("email").strip():
        return jsonify({"error": "Email is required"}), 400
    
    # Check if password is provided and meets minimum length
    # Passwords should be at least 6 characters long for basic security
    password = data.get("password", "")
    if not password or len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long"}), 400
    
    # Check if role_id is provided
    if not data.get("role_id"):
        return jsonify({"error": "Role ID is required"}), 400
    
    # DUPLICATE CHECK: Make sure this email doesn't already exist
    # Admin.query.filter_by(email=...) searches for an admin with this email
    existing_admin = Admin.query.filter_by(email=data.get("email").strip()).first()
    if existing_admin:
        # If we find an admin with this email, reject the request
        return jsonify({"error": "An admin with this email already exists"}), 400
    
    # ROLE VALIDATION: Make sure the role_id actually exists in the database
    role = Role.query.get(data.get("role_id"))
    if not role:
        return jsonify({"error": "Invalid role ID - role does not exist"}), 404
    
    # All validation passed! Now create the admin
    admin = Admin(                                         # Create a new admin
        full_name=data.get("full_name").strip(),          # .strip() removes extra spaces
        email=data.get("email").strip().lower(),          # .lower() converts to lowercase for consistency
        role=role
    )

    admin.set_password(password)                           # Encrypt and save the admin password.
    
    # ERROR HANDLING: Wrap database operations in try-except
    # This catches any errors that happen when saving to the database
    try:
        db.session.add(admin)
        db.session.commit()                                # Save the new admin to the database.
        return jsonify(admin.to_dict()), 201               # Return created admin information.
    
    except IntegrityError as e:
        # IntegrityError happens when we violate database constraints
        # For example: duplicate email, missing required field, etc.
        db.session.rollback()  # Undo any changes to keep database clean
        return jsonify({
            "error": "Database integrity error",
            "message": "This email might already be in use or data is invalid"
        }), 400
    
    except SQLAlchemyError as e:
        # SQLAlchemyError catches any other database-related errors
        # For example: connection lost, database is down, etc.
        db.session.rollback()  # Undo any changes
        return jsonify({
            "error": "Database error",
            "message": "Failed to create admin account. Please try again later."
        }), 500


# Updates existing admin information.
@admin_bp.route("/<int:admin_id>", methods=["PUT"])
@permission_required("manage_admins")
def update_admin(admin_id):

    admin = Admin.query.get_or_404(admin_id)                   # Find admin by ID or return 404 if not found.
    data = request.get_json() or {}                            # Get updated data from request.
    
    # VALIDATION: If full_name is provided, make sure it's not empty
    if "full_name" in data:
        if not data["full_name"] or not data["full_name"].strip():
            return jsonify({"error": "Full name cannot be empty"}), 400
        admin.full_name = data["full_name"].strip()
    
    # Update is_active status if provided
    if "is_active" in data:
        admin.is_active = data.get("is_active")

    # ROLE UPDATE: If a new role is provided, validate it exists
    if data.get("role_id"):
        role = Role.query.get(data["role_id"])
        if not role:
            return jsonify({"error": "Invalid role ID - role does not exist"}), 404
        admin.role = role

    # ERROR HANDLING: Wrap database commit in try-except
    try:
        db.session.commit()                                # Save changes.
        return jsonify(admin.to_dict()), 200
    
    except SQLAlchemyError as e:
        # Catch any database errors during update
        db.session.rollback()  # Undo any changes
        return jsonify({
            "error": "Database error",
            "message": "Failed to update admin. Please try again later."
        }), 500


# Deletes an admin from the database.
@admin_bp.route("/<int:admin_id>", methods=["DELETE"])
@permission_required("manage_admins")
def delete_admin(admin_id):

    admin = Admin.query.get_or_404(admin_id)                    # Find admin or return 404 if not found.
    
    # ERROR HANDLING: Wrap deletion in try-except
    try:
        db.session.delete(admin)
        db.session.commit()                                     # Remove admin from database.
        return jsonify({"message": "Admin deleted successfully"}), 200
    
    except IntegrityError as e:
        # IntegrityError might happen if this admin is referenced elsewhere
        # For example: if products are assigned to this admin
        db.session.rollback()
        return jsonify({
            "error": "Cannot delete admin",
            "message": "This admin has associated records. Update or remove them first."
        }), 400
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            "error": "Database error",
            "message": "Failed to delete admin. Please try again later."
        }), 500
