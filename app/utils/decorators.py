from functools import wraps   # Imports wraps to preserve the original function's information when using decorators.

from flask import jsonify  # Imports jsonify to return JSON responses.

from flask_jwt_extended import verify_jwt_in_request, get_jwt   # Imports JWT functions
# verify_jwt_in_request() checks if the user has a valid JWT token.
# get_jwt() retrieves the data stored inside the token.


# permission_required(): a custom decorator used to protect API routes based on user permissions.
def permission_required(*codes):                   # Creates a decorator that requires specific permissions.
    def decorator(fn):                             # Receives the function that needs permission checking.
        @wraps(fn)                                 # Keeps the original function name and metadata.

        def wrapper(*args, **kwargs):              # Wrapper function that runs before the protected function.
            verify_jwt_in_request()                # Ensures the request contains a valid JWT token
            claims = get_jwt()                     # Gets user information stored in the JWT token.

            if claims.get("role") == "super_admin": # Allows super admins to bypass permission checks.
                return fn(*args, **kwargs)
            
            if not set(claims.get("permissions", [])).intersection(codes): # Checks if the user's permissions match the required permissions.
                return jsonify({"error": "Forbidden"}), 403               # Returns a 403 error if the user lacks permission.

            return fn(*args, **kwargs)    # Allows access if the user has the required permission.

        return wrapper                    # Returns the protected function.

    return decorator                      # Returns the permission-checking decorator.