# This controller manages admin CRUD operations

from flask import Blueprint, request, jsonify
# Blueprint creates a group of related routes,
# request gets data sent by the client,
# jsonify returns JSON responses.

from app.extensions import db  # Import database connection.

from app.models import Admin, Role  # Import Admin model and Role model from the database.




# Creating an Admin Blueprint.
admin_bp = Blueprint("admins", __name__, url_prefix="/api/admins")


# Returns a list of all admins.
# Only users with "manage_admins" permission can access.
@admin_bp.route("", methods=["GET"])
def list_admins():
    return jsonify([a.to_dict() for a in Admin.query.all()]), 200


# Creates a new admin account.
# Receives admin details from the request body.
@admin_bp.route("", methods=["POST"])
def create_admin():

    data = request.get_json() or {}                        # Get JSON data from client
    admin = Admin(                                         # Create a new admin
        full_name=data.get("full_name"),
        email=data.get("email"),
        role=Role.query.get(data.get("role_id")))

    admin.set_password(data.get("password", ""))             # Encrypt and save the admin password.
    db.session.add(admin)
    db.session.commit()                                      # Save the new admin to the database.
    return jsonify(admin.to_dict()), 201                     # Return created admin information.


# Updates existing admin information.
@admin_bp.route("/<int:admin_id>", methods=["PUT"])
def update_admin(admin_id):

    admin = Admin.query.get_or_404(admin_id)                   # Find admin by ID or return 404 if not found.
    data = request.get_json() or {}                            # Get updated data from request.
    admin.full_name = data.get("full_name", admin.full_name)   # Update admin fields.
    admin.is_active = data.get("is_active", admin.is_active)

    if data.get("role_id"):                                    # Update role if a new role ID is provided.
        admin.role = Role.query.get(data["role_id"])

    db.session.commit()                                         # Save changes.
    return jsonify(admin.to_dict()), 200


# Deletes an admin from the database.
@admin_bp.route("/<int:admin_id>", methods=["DELETE"])
def delete_admin(admin_id):

    admin = Admin.query.get_or_404(admin_id)                    # Find admin or return 404 if not found.
    db.session.delete(admin)
    db.session.commit()                                          # Remove admin from database.
    return jsonify({"message": "Admin deleted"}), 200             # Return success message.
