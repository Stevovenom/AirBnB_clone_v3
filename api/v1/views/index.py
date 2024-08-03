#!/usr/bin/python3
"""Index"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieve the number of each object by type"""
    stats = {}
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    for cls in classes:
        cls_obj = getattr(models, cls, None)
        if cls_obj:
            stats[cls.lower() + 's'] = storage.count(cls_obj)
    return jsonify(stats)
