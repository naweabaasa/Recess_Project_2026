# This controller manages customer authentication.

from flask import Blueprint, request, jsonify  # Import Flask tools
# Blueprint creates routes,
# request receives client data,s
# jsonify returns JSON responses.

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity   # Import JWT function

from app.extensions import db          # Import database connection.# create_access_token creates login tokens,
# jwt_required protects private routes,
# get_jwt_identity gets the logged-in customer's ID.

from app.models import Customer      # Import Customer database model.


# Create Customer Blueprint.
customer_bp = Blueprint("customers", __name__, url_prefix="/api/customers")


# Creates a new customer account.
@customer_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json() or {}                # Get registration data from request body.
    customer = Customer(                           # Create a new customer.
        full_name=data.get("full_name"),
        email=data.get("email"),
        phone_number=data.get("phone_number"),
        address=data.get("address"),
    )

    # Encrypt and store customer password.
    customer.set_password(data.get("password", ""))

    # Save customer information in database.
    db.session.add(customer)
    db.session.commit()

    # Generate JWT token for the new customer.
    token = create_access_token(identity=str(customer.id))

    # Return customer details and login token.
    return jsonify({
        "customer": customer.to_dict(),
        "access_token": token
    }), 201


# Authenticates an existing customer.
@customer_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json() or {}                                             # Get login information.
    customer = Customer.query.filter_by(email=data.get("email")).first()        # Find customer using email.

    # Check if customer exists and password is correct.
    if not customer or not customer.check_password(data.get("password", "")):
        return jsonify({"error": "Invalid email or password"}), 401

    # Create JWT token after successful login.
    token = create_access_token(identity=str(customer.id))
    return jsonify({                                                              # Return customer details and access token.
        "customer": customer.to_dict(),
        "access_token": token
    }), 200


# Returns the profile of the logged-in customer.
@customer_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    customer_id = int(get_jwt_identity())  # Get logged-in customer ID from JWT token
    customer = Customer.query.get_or_404(customer_id)

    return jsonify(customer.to_dict()), 200    # Return customer profile information.
