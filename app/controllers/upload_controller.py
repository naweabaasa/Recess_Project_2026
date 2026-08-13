import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.utils.decorators import permission_required

# Create Upload Blueprint
upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")

# Allowed file extensions for images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _save_upload(file, subfolder):
    """Save an uploaded image to frontend/public/images/<subfolder>/ and return its URL."""
    import time
    filename = secure_filename(file.filename)
    timestamp = int(time.time())
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{timestamp}{ext}"

    dest_dir = os.path.join(
        current_app.root_path, '..', '..', 'frontend', 'public', 'images', subfolder
    )
    os.makedirs(dest_dir, exist_ok=True)
    file.save(os.path.join(dest_dir, filename))
    return f"/images/{subfolder}/{filename}"


@upload_bp.route("/product-image", methods=["POST"])
@permission_required("manage_products")
def upload_product_image():
    """
    Upload a product image file.

    Expects:
    - A file in the 'image' field of a multipart/form-data request

    Returns:
    - JSON with the image URL path
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg, gif, webp"}), 400

    try:
        image_url = _save_upload(file, "products")
        return jsonify({"message": "Image uploaded successfully", "image_url": image_url}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to upload image: {str(e)}"}), 500


@upload_bp.route("/hero-image", methods=["POST"])
@permission_required("manage_pages", "manage_products", "manage_orders")
def upload_hero_image():
    """
    Upload a hero slideshow image for the home page.

    Expects:
    - A file in the 'image' field of a multipart/form-data request

    Returns:
    - JSON with the image URL path (saved under /images/hero/)
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg, gif, webp"}), 400

    try:
        image_url = _save_upload(file, "hero")
        return jsonify({"message": "Hero image uploaded successfully", "image_url": image_url}), 201
    except Exception as e:
        return jsonify({"error": f"Failed to upload hero image: {str(e)}"}), 500
