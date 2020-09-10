#!/usr/bin/python3
"""
Module for Place - Amenity
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
import models
import os


@app_views.route('/places/<string:place_id>/amenities', 
                 strict_slashes=False, methods=['GET'])
def pl_am_all(place_id):
    """
    Lists all amenity objects of a place
    Raise 404 error if place_id is not linked to any place
    """
    place_holder = models.storage.get("Place", place_id)
    if place_holder is None:
        abort(404)

    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_obj = place_holder.amenities
    else:
        amenity_obj = place_holder.amenity_ids

    for amen in amenity_obj:
        amenities.append(amen.to_dict())
        return_helper = jsonify(amenities)
    return return_helper
