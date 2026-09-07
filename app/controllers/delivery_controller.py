from flask import Blueprint, request, jsonify
from app.extensions import db    # Import database connection.
from app.models import Delivery    # Import Delivery database model.
from app.utils.decorators import permission_required  # Import permission decorator


# Create Delivery Blueprint.
delivery_bp = Blueprint("deliveries", __name__, url_prefix="/api/deliveries")


# Retrieves all delivery records.
# Requires "manage_deliveries" permission.
@delivery_bp.route("", methods=["GET"])
@permission_required("manage_deliveries")
def list_deliveries():
    # Load deliveries with their related orders, ordered newest first
    deliveries = Delivery.query.join(Delivery.order).order_by(Delivery.id.desc()).all()
    
    # Return all deliveries as JSON.
    return jsonify([d.to_dict() for d in deliveries]), 200


# Retrieves a single delivery by ID.
@delivery_bp.route("/<int:delivery_id>", methods=["GET"])
@permission_required("manage_deliveries")
def get_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    return jsonify(delivery.to_dict()), 200


# Creates a new delivery record.
@delivery_bp.route("", methods=["POST"])
@permission_required("manage_deliveries")
def create_delivery():

    data = request.get_json() or {}                      # Get delivery data from request body.
    delivery = Delivery(                                 # Create a new delivery object.
        order_id=data.get("order_id"),
        delivery_address=data.get("delivery_address"),
        status=data.get("status", "pending")
    )

    db.session.add(delivery)                              # Save delivery information to database.
    db.session.commit()
    return jsonify(delivery.to_dict()), 201               # Return created delivery details.


# Updates an existing delivery status and details.
@delivery_bp.route("/<int:delivery_id>", methods=["PUT"])
@permission_required("manage_deliveries")
def update_delivery(delivery_id):

    delivery = Delivery.query.get_or_404(delivery_id)       # Find delivery by ID or return 404 if not found.

    data = request.get_json() or {}                          # Get updated data.
    if "status" in data:
        delivery.status = data["status"]
    if "delivery_address" in data:
        delivery.delivery_address = data["delivery_address"]
        if delivery.order:
            delivery.order.delivery_address = data["delivery_address"]
    if "delivery_date" in data:
        delivery.delivery_date = data["delivery_date"]

    try:
        db.session.commit()                           # Save changes.
        return jsonify(delivery.to_dict()), 200       # Return updated delivery details.
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update delivery", "details": str(e)}), 500


# Deletes a delivery record.
@delivery_bp.route("/<int:delivery_id>", methods=["DELETE"])
@permission_required("manage_deliveries")
def delete_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    try:
        if delivery.order:
            delivery.order.delivery_required = False
        db.session.delete(delivery)
        db.session.commit()
        return jsonify({"message": "Delivery deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete delivery", "details": str(e)}), 500
