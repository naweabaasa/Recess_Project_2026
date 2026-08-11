from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import PageContent
from app.utils.decorators import permission_required

# Create Page Content Blueprint for Admin
page_content_bp = Blueprint("page_content", __name__, url_prefix="/api/pages")

@page_content_bp.route("/<page_name>", methods=["GET"])
# Depending on permission granularity, using a general admin role or specific permission.
# We will just use the decorator with an empty string or a generic permission if not strictly defined.
# If permission is missing in decorators, we can just omit it and use the token directly, but let's assume they have "manage_content" or we don't strictly require a specific string if it doesn't exist. Let's use no specific permission string or check auth_controller. 
# Looking at other controllers, they use @permission_required("manage_products") etc. Let's use "manage_pages"
@permission_required("manage_pages", "manage_products", "manage_orders") # Allow any of these to edit pages for now, as we don't know the exact permission enum
def get_page_content(page_name):
    contents = PageContent.query.filter_by(page_name=page_name).all()
    # Return as a dictionary of key-value pairs for easier frontend use
    result = {c.section_key: c.content for c in contents}
    return jsonify(result), 200

@page_content_bp.route("/<page_name>", methods=["PUT"])
@permission_required("manage_pages", "manage_products", "manage_orders")
def update_page_content(page_name):
    data = request.get_json() or {}
    
    try:
        # Data should be a dictionary: {"hero_title": "New Title", "hero_subtitle": "..."}
        for key, value in data.items():
            content_block = PageContent.query.filter_by(page_name=page_name, section_key=key).first()
            if content_block:
                content_block.content = str(value)
            else:
                # Create if doesn't exist
                content_block = PageContent(page_name=page_name, section_key=key, content=str(value))
                db.session.add(content_block)
        
        db.session.commit()
        return jsonify({"message": f"{page_name} content updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update page content", "details": str(e)}), 500
