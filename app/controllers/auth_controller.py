from flask import Blueprint, request, jsonify 
from flask_jwt_extended import (     
    create_access_token, create_refresh_token,     
    jwt_required, get_jwt_identity, get_jwt   
) 
from app.extensions import db 
from app.models import User, Role   


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")     
def _claims_for(user: User):     
    """Bake role + permission codes into the token so every request     
    doesn't need a DB round trip to check access."""     
    return {         "role": user.role.name if user.role else None,         
            "permissions": [p.code for p in user.role.permissions] if user.role else [],    
            }    
    def create_tokens(user: User):     
        claims = _claims_for(user)     
        access_token = create_access_token(identity=str(user.id), additional_claims=claims)     
        refresh_token = create_refresh_token(identity=str(user.id), additional_claims=claims)     
        return access_token, refresh_token     
   
   
    @auth_bp.route("/register", methods=["POST"]) 
    def register():     """     
    Public registration is optional for a marketing site. Most teams will     
    instead have a super_admin create staff accounts via /api/users.     
    Kept here for the initial 'client' self-signup case, defaults to the     
    lowest-privilege role.     """     
    data = request.get_json() or {}     
    required = ["full_name", "email", "password"]     
    if not all(data.get(f) for f in required):         
        return jsonify({"error": "full_name, email and password are required"}), 400       
    if User.query.filter_by(email=data["email"].lower().strip()).first():         
        return jsonify({"error": "Email already registered"}), 409       
    default_role = Role.query.filter_by(name="client").first()     
    if not default_role:         
        return jsonify({"error": "Default role not seeded yet"}), 500       
    
    user = User(         
        full_name=data["full_name"].strip(),         
        email=data["email"].lower().strip(),         
        role=default_role,     )     
    user.set_password(data["password"])     
    db.session.add(user)     
    db.session.commit()       
    
    access_token, refresh_token = create_tokens(user)     
    return jsonify({         
        "user": user.to_dict(),         
        "access_token": access_token,         
        "refresh_token": refresh_token,     
    }), 201     


@auth_bp.route("/login", methods=["POST"]) 
def login():     
    
    data = request.get_json() or {}     
    email = (data.get("email") or "").lower().strip()     
    password = data.get("password") or ""       
    user = User.query.filter_by(email=email).first()     
    if not user or not user.check_password(password):         
        return jsonify({"error": "Invalid email or password"}), 401     
    
    if not user.is_active:         
        return jsonify({"error": "Account is disabled"}), 403       
    
    access_token, refresh_token = create_tokens(user)     
    return jsonify({         
        "user": user.to_dict(),         
        "access_token": access_token,         
        "refresh_token": refresh_token,     
    }), 200     


@auth_bp.route("/refresh", methods=["POST"]) 
@jwt_required(refresh=True) 

def refresh():     
    user_id = get_jwt_identity()     
    user = User.query.get_or_404(user_id)     
    access_token, _ = create_tokens(user)     
    return jsonify({"access_token": access_token}), 200     



@auth_bp.route("/me", methods=["GET"]) 
@jwt_required() 

def me():     
    user_id = get_jwt_identity()     
    user = User.query.get_or_404(user_id)     
    return jsonify(user.to_dict()), 200 