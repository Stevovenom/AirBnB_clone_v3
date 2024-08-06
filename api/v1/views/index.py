#!/usr/bin/python3
"""Module definition for blueprint routes"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})

@app_views.route("/stats", strict_slashes=False)
def stats():
    """Retrieve the number of each object by type"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }

    return jsonify(stats)
