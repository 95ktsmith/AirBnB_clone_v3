#!/usr/bin/python3
"""
Module for Amenities
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
import models



@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def amenity_all():
    """
    State objects listed in their entirety
    """
    state_holder = []
    for state in models.storage.all("Amenity").values():
        state_holder.append(state.to_dict())
    return_holder = jsonify(state_holder)
    return return_holder

