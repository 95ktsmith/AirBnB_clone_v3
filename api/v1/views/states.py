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


