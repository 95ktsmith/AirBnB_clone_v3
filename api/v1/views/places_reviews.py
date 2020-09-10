#!/usr/bin/python3
"""
Module for Review
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
import models


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['GET'])
def review_all(place_id):
    """
    Review objects listed in their entirety
    """
    place = models.storage.get(Place, place_id)
    if place is None:
        abort(404)

    review_holder = []
    for review in models.storage.all(Review).values():
        if review.place_id == place.id:
            review_holder.append(review.to_dict())

    if review_holder is None:
        abort(404)

    return_holder = jsonify(review_holder)
    return return_holder


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def review_one(review_id):
    """
    Review object retrieved with 404 error handling
    when review_id is not linked to any Review object
    """
    review_one = models.storage.get(Review, review_id)
    if review_one is None:
        abort(404)
    return_holder = jsonify(review_one.to_dict())
    return return_holder


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def review_delete(review_id):
    """
    Review object deleted with 404 error handling
    if review_id is not linked to any Review object
    Return: Empty dictionary with status code 200
    """
    remove_help = models.storage.get("Review", review_id)
    if remove_help is None:
        abort(404)
    remove_help.delete()
    models.storage.save()
    return_holder = jsonify({})
    return return_holder


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False,
                 methods=['POST'])
def review_create(place_id):
    """
    Review created with specific parameters:
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - If dict doesn't contain key email raise error 400 w/ message
    Returns: New Review with status code 201
    """
    if models.storage.get(Place, place_id) is None:
        abort(404)

    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    if "user_id" not in request_help:
        return_holder = jsonify(error="Missing user_id")
        return make_response(return_holder, 400)
    if models.storage.get(User, request_help['user_id']) is None:
        abort(404)
    if "name" not in request_help:
        return_holder = jsonify(error="Missing name")
        return make_response(return_holder, 400)
    request_help["place_id"] = place_id
    create_help = models.review.Review(**request_help)
    create_help.save()
    return_holder = jsonify(create_help.to_dict())
    return make_response(return_holder, 200)


@app_views.route('/reviews/<string:review_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def review_update(review_id):
    """
    Review object updated with specific parameters:
    - If review_id is not linked to any User object raise 404 error
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - Update User object with all key-value pairs of the dict
    - Ignore keys: id, created_at and updated_at
    Return: Review object with the status code 200
    """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    ignore_these = ["id", "user_id", "place_id", "created_at", "updated_at"]
    update_help = models.storage.get("Review", review_id)
    if update_help is None:
        abort(404)
    for k_ey, v_al in request_help.items():
        if k_ey not in ignore_these:
            setattr(update_help, k_ey, v_al)
        update_help.save()
        return_holder = jsonify(update_help.to_dict())
        return return_holder
