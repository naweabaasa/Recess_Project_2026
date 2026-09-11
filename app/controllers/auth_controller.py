# Admin login
from flask import Blueprint, request, jsonify
# Blueprint creates a group of routes,
# request receives data from the client,
# jsonify returns JSON responses

from flask_jwt_extended import create_access_token   # Creates JWT authentication tokens.

from app.models import Admin  # Import Admin database model.


# Creating authentication Blueprint.
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# Handles admin login and generates an access token.
@auth_bp.route("/login", methods=["POST"])
def login():
    import traceback

    try:
        data = request.get_json() or {}                                 # Get login details sent by the user.
        admin = Admin.query.filter_by(email=data.get("email")).first()  # Find admin account using the provided email.

        # Check if admin exists and password is correct.
        # If login fails, return an error message.
        if not admin or not admin.check_password(data.get("password", "")):
            return jsonify({"error": "Invalid email or password"}), 401

        # Define all permissions that admins have access to
        # Since all logged-in admins should have full access, we grant all permissions
        all_permissions = [
            "manage_categories",
            "manage_products",
            "manage_orders",
            "manage_deliveries",
            "manage_page_content",
            "manage_admins"
        ]
        
        # Generate JWT access token with admin ID and all permissions
        token = create_access_token(
            identity=str(admin.id),
            additional_claims={"permissions": all_permissions}
        )

        # Return admin details and login token
        return jsonify({
            "admin": admin.to_dict(),
            "access_token": token
        }), 200
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        traceback_str = traceback.format_exc()
        print("LOGIN ERROR:", error_msg)
        print(traceback_str)
        return jsonify({"error": "Server error", "details": error_msg, "traceback": traceback_str}), 500
