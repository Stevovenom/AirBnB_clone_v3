#!/usr/bin/python3
"""Flask server (variable app)"""

from flask import Flask, jsonify
from models import storage
from models.state import State
from models.city import City
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.url_map.strict_slashes = False


@app.errorhandler(404)
def page_not_found(error):
    """Return a JSON response for a 404 error."""
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """Close the SQLAlchemy session."""
    storage.close()


@app.route('/api/v1/states', methods=['GET'])
def get_states():
    """Retrieve all states"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """Retrieve all cities in a given state"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@app.route('/api/v1/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieve a city by ID"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
