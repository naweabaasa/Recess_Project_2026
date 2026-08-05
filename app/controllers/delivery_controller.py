from flask import Blueprint, request, jsonify
from app.extensions import db    # Import database connection.
from app.models import Delivery    # Import Delivery database model.


# Create Delivery Blueprint.
delivery_bp = Blueprint("deliveries", __name__, url_prefix="/api/deliveries")


# Retrieves all delivery records.
# Requires "manage_delivery" permission.
@delivery_bp.route("", methods=["GET"])
def list_deliveries():

    # Return all deliveries as JSON.
    return jsonify([d.to_dict() for d in Delivery.query.all()]), 200


# Creates a new delivery record.
@delivery_bp.route("", methods=["POST"])
def create_delivery():

    data = request.get_json() or {}                      # Get delivery data from request body.
    delivery = Delivery(                                 # Create a new delivery object.
        order_id=data.get("order_id"),
        delivery_address=data.get("delivery_address"),
        delivery_fee=data.get("delivery_fee", 0),
        status=data.get("status", "pending")
    )

    db.session.add(delivery)                              # Save delivery information to database.
    db.session.commit()
    return jsonify(delivery.to_dict()), 201               # Return created delivery details.


# Updates an existing delivery status and date.
@delivery_bp.route("/<int:delivery_id>", methods=["PUT"])
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
