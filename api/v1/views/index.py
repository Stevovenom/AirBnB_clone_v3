#!/usr/bin/python3
from flask import jsonify
from . import app_views


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})
