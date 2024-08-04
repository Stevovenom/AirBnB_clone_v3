#!/usr/bin/python3
"""
New view for State objects that handles all default RESTFul API actions.
"""

from flask import Flask, abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieves the list of all State objects.
    """
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object by ID.

    Args:
        state_id (str): The ID of the State to retrieve.

    Returns:
        json: The state object in JSON format or a 404 error if not found.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object.

    Returns:
        json: The newly created state object in JSON format
        or appropriate errors.
    """
    response = request.get_json()
    if not response:
        abort(400, description="Not a JSON")
    if 'name' not in response:
        abort(400, description="Missing name")
    state = State(name=response['name'])
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object by ID.

    Args:
        state_id (str): The ID of the State to update.

    Returns:
        json: The updated state object in JSON format or appropriate errors.
    """
    response = request.get_json()
    if not response:
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object by ID.

    Args:
        state_id (str): The ID of the State to delete.

    Returns:
        json: An empty dictionary with a status code 200 or a 404 error
        if not found.
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
