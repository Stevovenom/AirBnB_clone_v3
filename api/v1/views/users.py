#!/usr/bin/python3
"""User objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, request, jsonify


@app_views.route("/users", strict_slashes=False, methods=["GET"])
@app_views.route("/users/<user_id>", strict_slashes=False, methods=["GET"])
def user(user_id=None):
    """Show user and user with ID"""
    if user_id is None:
        all_users = storage.all(User).values()
        user_list = [user.to_dict() for user in all_users]
        return jsonify(user_list)
    else:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["DELETE"])
def user_delete(user_id):
    """Delete a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """Create a new user"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    """Update a user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
