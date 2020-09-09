#!/usr/bin/python3
"""
Module for Amenities
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
from models.state import State
from models.city import City
import models


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def user_all():
    """
    User objects listed in their entirety
    """
    user_holder = []
    for user in models.storage.all("User").values():
        user_holder.append(state.to_dict())
    return_holder = jsonify(user_holder)
    return return_holder


@app_views.route('/users/<user_id>', strict_slashes=False, 
                 methods=['GET'])
def user_one(user_id):
    """
    User object retrieved with 404 error handling
    when user_id is not linked to any User object
    """
    user_one = models.storage.get("User", user_id)
    if user_one is None:
        abort(404)
    return_holder = jsonify(user_one.to_dict())
    return return_holder


@app_views.route('/user/<user_id>',
                 strict_slashes=False,
                 methods=['DELETE'])
def user_delete(user_id):
    """
    User object deleted with 404 error handling
    if user_id is not linked to any User object
    Return: Empty dictionary with status code 200
    """
    remove_help = models.storage.get("User", user_id)
    if remove_help is None:
        abort(404)
    remove_help.delete()
    models.storage.save()
    return_holder = jsonify({})
    return return_holder


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def user_create():
    """
    User created with specific parameters:
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - If dict doesn't contain key email raise error 400 w/ message
    Returns: New User with status code 201
    """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    if "email" not in request_help:
        return_holder = jsonify(error="Missing email")
        return make_response(return_holder, 400)
    create_help = models.user.User(**request_help)
    create_help.save()
    return_holder = jsonify(create_help.to_dict())
    return make_response(return_holder, 201)


@app_views.route('/users/<string:user_id>',
                 strict_slashes=False,
                 methods=['PUT'])
def user_update(user_id):
    """
    User object updated with specific parameters:
    - If user_id is not linked to any User object raise 404 error
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - Update User object with all key-value pairs of the dict
    - Ignore keys: id, created_at and updated_at
    Return: Amenity object with the status code 200
    """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    ignore_these = ["id", "created_at", "updated_at"]
    update_help = models.storage.get("User", user_id)
    if update_help is None:
        abort(404)
    for k_ey, v_al in request_help.items():
        if k_ey not in ignore_these:
            setattr(update_help, k_ey, v_al)
        update_help.save()
        return_holder = jsonify(update_help.to_dict())
        return return_holder
