#!/usr/bin/python3
"""
State objects that handle all default RESTFul API actions.
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.
    """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object.

    Args:
        state_id (str): The ID of the State to retrieve.

    Returns:
        json: The state object in JSON format or a 404 error if not found.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object.

    Args:
        state_id (str): The ID of the State to delete.

    Returns:
        json: An empty dictionary with a status code 200 or a 404 error if
        not found.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State.

    Returns:
        json: The newly created state object in JSON format or appropriate
        errors.
    """
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    data = request.get_json()
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object.

    Args:
        state_id (str): The ID of the State to update.

    Returns:
        json: The updated state object in JSON format or appropriate errors.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
