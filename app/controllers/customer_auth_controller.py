# Customer register/login
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Customer

customer_bp = Blueprint("customers", __name__, url_prefix="/api/customers")

@customer_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    customer = Customer(
        full_name=data.get("full_name"), email=data.get("email"),
        phone_number=data.get("phone_number"), address=data.get("address"),
    )
    customer.set_password(data.get("password", ""))
    db.session.add(customer)
    db.session.commit()

    token = create_access_token(identity=str(customer.id))
    return jsonify({"customer": customer.to_dict(), "access_token": token}), 201

@customer_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    customer = Customer.query.filter_by(email=data.get("email")).first()

    if not customer or not customer.check_password(data.get("password", "")):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(customer.id))
    return jsonify({"customer": customer.to_dict(), "access_token": token}), 200

@customer_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    customer = Customer.query.get_or_404(get_jwt_identity())
    return jsonify(customer.to_dict()), 200