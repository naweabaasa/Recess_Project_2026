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
    # Check if file is in request
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    # Check if user actually selected a file
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: png, jpg, jpeg, gif, webp"}), 400
    
    try:
        # Secure the filename to prevent directory traversal attacks
        filename = secure_filename(file.filename)
        
        # Add timestamp to filename to avoid conflicts
        import time
        timestamp = int(time.time())
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        # Define upload directory (relative to frontend public folder)
        # Save to frontend/public/images/products/
        frontend_images_dir = os.path.join(
            current_app.root_path, '..', '..', 'frontend', 'public', 'images', 'products'
        )
        
        # Create directory if it doesn't exist
        os.makedirs(frontend_images_dir, exist_ok=True)
        
        # Save the file
        filepath = os.path.join(frontend_images_dir, filename)
        file.save(filepath)
        
        # Return the URL path (relative to frontend public folder)
        image_url = f"/images/products/{filename}"
        
        return jsonify({
            "message": "Image uploaded successfully",
            "image_url": image_url
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Failed to upload image: {str(e)}"}), 500
