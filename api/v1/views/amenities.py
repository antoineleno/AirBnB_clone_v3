#!/usr/bin/python3
"""State module"""

from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"])
def view_all_amenity():
    """Method to view all amenity"""
    all_amenities = storage.all(Amenity).values()

    amenities = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def view_single_amenity(amenity_id):
    """View amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """Delete amenity base on its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"])
def post_an_amenity():
    """Method to to post an amenity"""
    if not request.json:
        return abort(400, "Not a JSON")
    arguments = request.get_json()
    if "name" not in arguments:
        return abort(400, "Missing name")
    amenity = State(**arguments)
    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id", methods=["PUT"])
def update_single_amnity(amenity_id):
    """Update a State object by id"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    amenity = storage.get(State, amenity_id)
    if amenity is None:
        abort(404)

    arguments = request.get_json()

    if "name" not in arguments:
        abort(400, description="Missing name")

    for key, value in arguments.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
