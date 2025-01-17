#!/usr/bin/python3
"""
  route in object that returns a json
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """
    Return the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """
    It retrieves the number of each object type.
    """
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    return jsonify(stats)
