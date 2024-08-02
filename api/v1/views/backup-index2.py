#!/usr/bin/python3
from flask import jsonify
from models import storage


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Retrieve the number of each object by type"""
    stats = {}
    classes = ["Amenity", "City", "Place", "Review", "State", "User"]
    for cls in classes:
        # Get the class from the storage module
        cls_obj = getattr(models, cls, None)
        if cls_obj:
            stats[cls.lower() + 's'] = storage.count(cls_obj)
    return jsonify(stats)
