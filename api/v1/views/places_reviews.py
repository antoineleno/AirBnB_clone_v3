#!/usr/bin/python3
"""Review module"""

from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request

@app_views.route("/places/<place_id>/reviews", methods=["GET"])
def get_reviews_of_place(place_id):
    """Retrieve the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in storage.all(Review).values() if review.place_id == place_id]
    return jsonify(reviews)

@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """Retrieve a Review object by its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    
    return jsonify(review.to_dict())

@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """Delete a Review object by its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route("/places/<place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """Create a new Review object"""
    if not request.is_json:
        abort(400, "Not a JSON")
    
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    
    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")
    
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    
    if "text" not in data:
        abort(400, "Missing text")
    
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route("/reviews/<review_id>", methods=["PUT"])
def update_review(review_id):
    """Update a Review object by its id"""
    if not request.is_json:
        abort(400, "Not a JSON")
    
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    
    data = request.get_json()
    if "text" not in data:
        abort(400, "Missing text")

    for key, value in data.items():
        if key not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    
    review.save()
    return jsonify(review.to_dict()), 200
