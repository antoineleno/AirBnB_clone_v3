#!/usr/bin/python3
"""place module"""

from models.place import Place
from models.city import City
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def view_all_places(city_id):
    """Method to view all places"""
    place = storage.get(Place, city_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["GET"])
def view_single_place(place_id):
    """View place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Delete place base on its id"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def post_a_place(city_id):
    """Method to to post a place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        return abort(400, "Not a JSON")
    arguments = request.get_json()
    if "user_id" not in arguments:
        return abort(400, "Missing user_id")
    elif "name" not in arguments:
        return abort(400, "Missing name")

    place = Place(**arguments)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_single_place(place_id):
    """Update a place object by id"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    arguments = request.get_json()

    for key, value in arguments.items():
        if key not in ["user_id", "city_id", "created_at", "updated_at"]:
            setattr(City, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
