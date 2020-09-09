#!/usr/bin/python3
"""
Module for States
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
import models


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def state_all():
    """
    State objects listed in their entirety
    """
    state_holder = []
    for state in models.storage.all("State").values():
        state_holder.append(state.to_dict())
    return_holder = jsonify(state_holder)
    return return_holder


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def state_one(state_id):
    """
    State object retrieved with 404 error handling
    when state_id is not linked to any State object
    """
    state_one = models.storage.get("State", state_id)
    if state_one is None:
        abort(404)
    return_holder = jsonify(state_one.to_dict())
    return return_holder


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['DELETE'])
def state_delete(state_id):
    """
    State object deleted with 404 error handling
    if state_id is not linked to any State object
    Return: Empty dictionary with status code 200
    """
    remove_help = models.storage.get("State", state_id)
    if remove_help if None:
        abort(404)
    remove_help.delete()
    models.storage.save()
    return_holder = jsonify({})
    return return_holder


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def state_create():
    """
    State created with specific parameters:
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - If dict doesn't contain key name raise error 400 w/ message
    Returns: New State with status code 201
    """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    if "name" not in request_help:
        return_holder = jsonify(error="Missing name")
        return make_response(return_holder, 400)
    create_help = models.state.State(**request_help)
    create_help.save()
    return_holder = jsonify(create_help.to_dict())
    return make_response(return_holder, 201)


@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['PUT'])
def state_update(state_id):
    """
    State object updated with specific parameters:
    - If state_id is not linked to any State object raise 404 error
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - Update State object with all key-value pairs of the dict
    - Ignore keys: id, created_at and updated_at
    Return: State object with the status code 200
    """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    ignore_these = ["id", "created_at", "updated_at"]
    update_help = models.storage.get("State", state_id)
    if update_help is None:
        abort(404)
    for k_ey, v_al in request_help.items():
        if k_ey not in ignore_these:
            setattr(update_help, k_ey, v_al)
        update_help.save()
        return_holder = jsonify(update_help.to_dict())
        return return_holder
