#!/usr/bin/python3
"""
Module for Place
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
from models.state import State
from models.city import City
import models


@app_views.route('/places', strict_slashes=False, methods=['GET'])
def place_all(city_id):
    """
    Place objects listed in their entirety
    """
    place_holder = []
    for place in models.storage.all("Place").values():
        place_holder.append(place.to_dict())
    return_holder = jsonify(place_holder)
    return return_holder


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def place_one(place_id):
    """
    Place object retrieved with 404 error handling
    when place_id is not linked to any Place object
    """
    place_one = models.storage.get("Place", place_id)
    if place_one is None:
        abort(404)
    return_holder = jsonify(place_one.to_dict())
    return return_holder


@app_views.route('/places/<place_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def place_delete(place_id):
    """
    Place object deleted with 404 error handling
    if place_id is not linked to any Place object
    Return: Empty dictionary with status code 200
    """
    remove_help = models.storage.get("Place", place_id)
    if remove_help is None:
        abort(404)
    remove_help.delete()
    models.storage.save()
    return_holder = jsonify({})
    return return_holder


@app_views.route('/places', strict_slashes=False, methods=['POST'])
def place_create(city_id):
    """
    Place created with specific parameters:
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - If dict doesn't contain key email raise error 400 w/ message
    Returns: New Place with status code 201
    """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    if "user_id" not in request_help:
        return_holder = jsonify(error="Missing user_id")
        return make_response(return_holder, 400)
    if "name" not in request_help:
        return_holder = jsonify(error="Missing name")
        return make_response(return_holder, 400)
    create_help = models.user.Place(**request_help)
    create_help.save()
    return_holder = jsonify(create_help.to_dict())
    return make_response(return_holder, 201)


@app_views.route('/places/<string:place_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def place_update(place_id):
    """
    Place object updated with specific parameters:
    - If place_id is not linked to any User object raise 404 error
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - Update User object with all key-value pairs of the dict
    - Ignore keys: id, created_at and updated_at
    Return: Place object with the status code 200
    """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    ignore_these = ["id", "created_at", "updated_at"]
    update_help = models.storage.get("Place", place_id)
    if update_help is None:
        abort(404)
    for k_ey, v_al in request_help.items():
        if k_ey not in ignore_these:
            setattr(update_help, k_ey, v_al)
        update_help.save()
        return_holder = jsonify(update_help.to_dict())
        return return_holder
