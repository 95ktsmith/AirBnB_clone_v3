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


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>', 
                 strict_slashes=False, methods=['DELETE'])
def pl_am_delete(place_id, amenity_id):
    """
    Deletes Amenity object to Place with specific parameters:
    - If place_id is not linked to Place obj, raise 404 error
    - If amenity_id is not linked to Amenity obj, raise 404 error
    - If Amenity is not linked to Place before request, raise 404 error
    Returns: Empty dictionary with status code 200
    """
    place_holder = models.storage.get("Place", place_id)
    amen_holder = models.storage.get("Amenity", amenity_id)
    if place_holder is None or amen_holder is None:
        abort(404)
    if amen_holder not in amenity_obj:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_obj = place_holder.amenities
    else:
        amenity_obj = place_holder.amenity_ids

    amenity_obj.delete(amenity_obj)
    amenity_obj.save()
    return_helper = jsonify({})
    return return_helper


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 strict_slashes=False, methods=['POST'])
def pl_am_post(place_id, amenity_id):
    """
    Link Amenity object to Place with specifications:
    - No HTTP body needed
    - If place_id is not linked to Place obj, raise 404 error
    - If amenity_id is not linked to Amenity obj, raise 404 error
    - If Amenity is already linked to Place, return Amenity w status code 200
    Returns: Amenity with status code 201
    """
    place_holder = models.storage.get("Place", place_id)
    amen_holder = models.storage.get("Amenity", amenity_id)
    if place_holder is None or amen_holder is None:
        abort(404)
    if amen_holder not in amenity_obj:
        abort(404)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_obj = place_holder.amenities
    else:
        amenity_obj = place_holder.amenity_ids

    if amen_holder in amenity_obj:
        return_helper = jsonify(amen_holder.to_dict())
        return return_helper
    amenity_obj.append(amen_holder)
    amenity_obj.save()
    return_helper = jsonify(amen_holder.to_dict())
    return return_helper
