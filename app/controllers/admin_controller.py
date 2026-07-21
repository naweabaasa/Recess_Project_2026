from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Admin, Role
from app.utils.decorators import permission_required

admin_bp = Blueprint("admins", __name__, url_prefix="/api/admins")

@admin_bp.route("", methods=["GET"])
@permission_required("manage_admins")
def list_admins():
    return jsonify([a.to_dict() for a in Admin.query.all()]), 200

@admin_bp.route("", methods=["POST"])
@permission_required("manage_admins")
def create_admin():
    data = request.get_json() or {}
    admin = Admin(full_name=data.get("full_name"), email=data.get("email"),
                  role=Role.query.get(data.get("role_id")))
    admin.set_password(data.get("password", ""))
    db.session.add(admin)
    db.session.commit()
    return jsonify(admin.to_dict()), 201

@admin_bp.route("/<int:admin_id>", methods=["PUT"])
@permission_required("manage_admins")
def update_admin(admin_id):
    admin = Admin.query.get_or_404(admin_id)
    data = request.get_json() or {}
    admin.full_name = data.get("full_name", admin.full_name)
    admin.is_active = data.get("is_active", admin.is_active)
    if data.get("role_id"):
        admin.role = Role.query.get(data["role_id"])
    db.session.commit()
    return jsonify(admin.to_dict()), 200

@admin_bp.route("/<int:admin_id>", methods=["DELETE"])
@permission_required("manage_admins")
def delete_admin(admin_id):
    admin = Admin.query.get_or_404(admin_id)
    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin deleted"}), 200