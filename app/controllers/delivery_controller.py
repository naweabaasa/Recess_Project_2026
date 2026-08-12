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
    # Load deliveries with their related orders
    deliveries = Delivery.query.join(Delivery.order).all()
    
    # Return all deliveries as JSON.
    return jsonify([d.to_dict() for d in deliveries]), 200


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


# Updates an existing delivery status and date.
@delivery_bp.route("/<int:delivery_id>", methods=["PUT"])
@permission_required("manage_deliveries")
def update_delivery(delivery_id):

    delivery = Delivery.query.get_or_404(delivery_id)       # Find delivery by ID or return 404 if not found.

    data = request.get_json() or {}                          # Get updated data.
    delivery.status = data.get("status", delivery.status)    # Update delivery status.
    delivery.delivery_date = data.get(                       # Update delivery date.
        "delivery_date",
        delivery.delivery_date
    )

    db.session.commit()                           # Save changes.
    return jsonify(delivery.to_dict()), 200       # Return updated delivery details.
