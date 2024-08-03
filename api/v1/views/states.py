#!/usr/bin/python3
"""State module"""

from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request

@app_views.route("/states", methods=["GET"])
def view_all_states():
    """Retrieve the list of all State objects"""
    all_states = storage.all(State).values()
    states = [state.to_dict() for state in all_states]
    return jsonify(states)

@app_views.route("/states/<state_id>", methods=["GET"])
def view_single_state(state_id):
    """Retrieve a State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete a State object by id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route("/states", methods=["POST"])
def post_a_state():
    """Create a new State object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    arguments = request.get_json()
    if "name" not in arguments:
        abort(400, description="Missing name")
    state = State(**arguments)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route("/states/<state_id>", methods=["PUT"])
def update_single_state(state_id):
    """Update a State object by id"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    arguments = request.get_json()

    if "name" not in arguments:
        abort(400, description="Missing name")

    for key, value in arguments.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_dict()), 200
