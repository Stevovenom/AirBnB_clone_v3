#!/usr/bin/python3
"""Module definitin setup Users route api"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User
from werkzeug.exceptions import BadRequest


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """Retrieve all users in the database"""
    users_list = []
    users = storage.all(User)
    for user in users.values():
        users_list.append(user.to_dict())

    return jsonify(users_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new user in the database"""
    try:
        user_data = request.get_json(force=True)
    except BadRequest:
        abort(400, 'Not a JSON')

    if "email" not in user_data:
        abort(400, 'Missing email')
    if "password" not in user_data:
        abort(400, 'Missing password')

    new_user = User(**user_data)
    new_user.save()
    response = jsonify(new_user.to_dict())
    response.status_code = 201

    return response


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieve a user details by ID"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Update an existing user object"""
    try:
        update_data = request.get_json()
    except BadRequest:
        abort(400, 'Not a JSON')

    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    for key, value in update_data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a user"""
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({})
