#!/usr/bin/python3
"""Module definition for blueprint of City objects"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities(state_id):
    """Return all City objects of a State, using the state ID"""
    city_list = []
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    all_cities = state_obj.cities
    for city in all_cities:
        city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<city_id>",  methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Return a city object, identifying it by it's ID"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a City object from the database using it's ID"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new City object using a state ID"""
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("State", str(state_id)):
        abort(404)
    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id
    new_city = City(**city_json)
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Update a City object with json input"""
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    city_obj = storage.get("City", str(city_id))
    if city_obj is None:
        abort(404)

    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city_obj, key, val)
    city_obj.save()
    return jsonify(city_obj.to_dict())
