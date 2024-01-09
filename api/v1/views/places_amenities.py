#!/usr/bin/python3
"""
Creates new view for the link between Place objects and Amenity objects that
handles all default RESTFul API actions
"""
from app.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import abort, jsonify, request
from os import getenv


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def amenities_get(place_id):
    """ Retrieves the list of all Amenity objects of a Place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        a = [amenity.to_dict() for amenity in place.amenities]
    else:
        a = [storage.get("Amenity", id).to_dict() for id in place.amenity_ids]
    return jsonify(a)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_del(place_id, amenity_id):
    """ Deletes a Amenity object to a Place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        index = place.amenity_ids.index(amenity_id)
        place.amenity_ids.pop(index)

    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def amenity_post(place_id, amenity_id):
    """ Link a Amenity object to a Place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)

    storage.save()
    return jsonify(amenity.to_dict()), 201
