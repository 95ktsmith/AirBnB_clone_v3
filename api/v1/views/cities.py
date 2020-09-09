#!/usr/bin/python3
"""
Module for Cities
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
from models.state import State
from models.city import City
import models


@app_views.route('/<state_id>/cities', strict_slashes=False, methods=['GET'])
def city_all(state_id):
    """
    Lists all cities related to a specified city id.
    Raises 404 error if city with given id is not found.
    """
    state = models.storage.get(State, state_id)
    if state is None:
        abort(404)

    city_holder = []
    for city in state.cities:
        city_holder.append(city.to_dict())
    return_holder = jsonify(city_holder)
    return return_holder


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city_one(city_id):
    """
    City object retrieved with 404 error handling
    when city_id is not linked to any City object
    """
    city_one = models.storage.get(City, city_id)
    if city_one is None:
        abort(404)
    return_holder = jsonify(city_one.to_dict())
    return return_holder


@app_views.route('/cities/<city_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def city_delete(city_id):
    """
    City object deleted with 404 error handling
    if city_id is not linked to any City object
    Return: Empty dictionary with status code 200
    """
    remove_help = models.storage.get("City", city_id)
    if remove_help is None:
        abort(404)
    remove_help.delete()
    models.storage.save()
    return_holder = jsonify({})
    return return_holder


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False,
                 methods=['POST'])
def city_create(state_id):
    """
    City created with specific parameters:
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If state_id is not linked to any state object, raise error 404
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - If dict doesn't contain key name raise error 400 w/ message
    Returns: New City with status code 201
    """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    if "name" not in request_help:
        return_holder = jsonify(error="Missing name")
        return make_response(return_holder, 400)
    if models.storage.get(State, state_id) is None:
        abort(404)
    request_help['state_id'] = state_id
    create_help = models.city.City(**request_help)
    create_help.save()
    return_holder = jsonify(create_help.to_dict())
    return make_response(return_holder, 201)


@app_views.route('/cities/<string:city_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def city_update(city_id):
    """
    City object updated with specific parameters:
    - If city_id is not linked to any City object raise 404 error
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - Update City object with all key-value pairs of the dict
    - Ignore keys: id, created_at and updated_at
    Return: City object with the status code 200
    """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    ignore_these = ["id", "created_at", "updated_at"]
    update_help = models.storage.get("City", city_id)
    if update_help is None:
        abort(404)
    for k_ey, v_al in request_help.items():
        if k_ey not in ignore_these:
            setattr(update_help, k_ey, v_al)
        update_help.save()
        return_holder = jsonify(update_help.to_dict())
        return return_holder
