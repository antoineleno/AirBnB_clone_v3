#!/usr/bin/python3
"""City module"""

from models.city import City
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request

@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities_of_state(state_id):
    """Retrieve the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in storage.all(City).values() if city.state_id == state_id]
    return jsonify(cities)

@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """Retrieve a City object by its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    return jsonify(city.to_dict())

@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """Delete a City object by its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """Create a new City object"""
    if not request.is_json:
        abort(400, "Not a JSON")
    
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    data = request.get_json()
    if "name" not in data:
        abort(400, "Missing name")
    
    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """Update a City object by its id"""
    if not request.is_json:
        abort(400, "Not a JSON")
    
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    data = request.get_json()
    if "name" not in data:
        abort(400, "Missing name")

    for key, value in data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    
    city.save()
    return jsonify(city.to_dict()), 200
