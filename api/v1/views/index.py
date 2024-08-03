#!/usr/bin/python3
"""Index"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """Returns the status of the API"""
    status = {
        "status": "OK"
    }

    response = jsonify(status)
    response.status_code = 200

    return response


@app_views.route("/stats", strict_slashes=False)
def stats():
    """Retrieve the number of each object by type"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "state": storage.count("State"),
        "users": storage.count("User")
    }

    response = jsonify(stats)
    response.status_code = 200

    return response
