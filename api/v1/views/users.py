#!/usr/bin/python3
"""User module"""

from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request

@app_views.route("/users", methods=["GET"])
def get_users():
    """Retrieve the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)

@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Retrieve a User object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    
    return jsonify(user.to_dict())

@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Delete a User object by its id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route("/users", methods=["POST"])
def create_user():
    """Create a new User object"""
    if not request.is_json:
        abort(400, "Not a JSON")
    
    data = request.get_json()
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201

@app_views.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Update a User object by its id"""
    if not request.is_json:
        abort(400, "Not a JSON")
    
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    
    data = request.get_json()
    if "email" in data:
        abort(400, "Cannot update email")

    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    
    user.save()
    return jsonify(user.to_dict()), 200
