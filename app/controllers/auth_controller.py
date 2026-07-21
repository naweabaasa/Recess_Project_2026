# Admin login 
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import Admin

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    admin = Admin.query.filter_by(email=data.get("email")).first()

    if not admin or not admin.check_password(data.get("password", "")):
        return jsonify({"error": "Invalid email or password"}), 401

    claims = {"role": admin.role.name, "permissions": [p.code for p in admin.role.permissions]}
    token = create_access_token(identity=str(admin.id), additional_claims=claims)
    return jsonify({"admin": admin.to_dict(), "access_token": token}), 200