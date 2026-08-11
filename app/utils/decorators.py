from functools import wraps   # Imports wraps to preserve the original function's information when using decorators.

from flask import jsonify  # Imports jsonify to return JSON responses.

from flask_jwt_extended import verify_jwt_in_request, get_jwt   # Import JWT functions.
# verify_jwt_in_request() checks if the user has a valid JWT token.
# get_jwt() retrieves the full JWT claims (payload) from the token.


# login_required(): a custom decorator used to protect API routes.
# It ensures only authenticated admins (with a valid JWT token) can access the route.
def login_required(fn):
    @wraps(fn)                                 # Keeps the original function name and metadata.
    def wrapper(*args, **kwargs):              # Wrapper function that runs before the protected function.
        verify_jwt_in_request()                # Ensures the request contains a valid JWT token.
        return fn(*args, **kwargs)             # Allows access if token is valid.
    return wrapper


# permission_required(): a custom decorator that checks if the logged-in admin
# has at least one of the specified permissions stored inside their JWT token claims.
# Usage: @permission_required("manage_products")
#    or: @permission_required("manage_brands", "manage_products")
def permission_required(*permissions):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()            # First ensure a valid JWT token is present.
            claims = get_jwt()                 # Read all claims from the token.
            user_permissions = claims.get("permissions", [])  # Get the permissions list.

            # Allow access if the user has ANY of the required permissions.
            if not any(p in user_permissions for p in permissions):
                return jsonify({
                    "error": "Access denied",
                    "message": f"You need one of these permissions: {', '.join(permissions)}"
                }), 403

            return fn(*args, **kwargs)         # Allow access if permission is present.
        return wrapper
    return decorator