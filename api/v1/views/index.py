#!/usr/bin/python3
"""Index module"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'])
def view_status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def view_count_states():
    """View count objects"""

    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    my_dict = {}
    for object in classes:
        my_dict[object] = storage.count(classes[object])

    return jsonify(my_dict)
