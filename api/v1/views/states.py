#!/usr/bin/python3
"""State module"""

from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route("/states", methods=["GET"])
def view_all_states():
    """Method to view all states"""
    all_states = storage.all(State).values()

    states = [state.to_dict() for state in all_states]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"])
def view_single_state(state_id):
    """View state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """Delete state base on its id"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/", methods=["POST"])
def post_a_state():
    """Method to view all states"""
    if not request.json:
        return abort(400, "Not a JSON")
    arguments = request.get_json()
    if "name" not in arguments:
        return abort(400, "Missing name")
    state = State(**arguments)
    state.save()
    return jsonify(state.to_dict()), 200

@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """update a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    state.save()
    return jsonify(state.to_dict())