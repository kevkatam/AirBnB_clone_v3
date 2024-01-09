#!/usr/bin/python3
"""
Create a new view for Review object that handles all default RESTFul
API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('places/<place_id>/reviews', strict_slashes=False)
def reviews_get(place_id):
    """ Retrieves the list of all Review objects of a Place """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def reviews_getid(review_id):
    """ Retrieves a Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def review_del(review_id):
    """ Deletes a Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    """ Creates a Review object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    newreview = request.get_json()
    if not newreview:
        abort(400, "Not a JSON")
    if 'user_id' not in newreview:
        abort(400, "Missing user_id")
    user_id = newreview['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if 'text' not in newreview:
        abort(400, "Missing text")
    review = Review(**newreview)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_put(review_id):
    """ Updates a Review object """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    request_body = request.get_json()
    if not request_body:
        abort(400, "Not a JSON")

    for ke, value in request_body.items():
        if ke not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, ke, value)
    storage.save()
    return jsonify(review.to_dict()), 200
