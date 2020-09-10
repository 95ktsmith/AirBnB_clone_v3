#!/usr/bin/python3
"""
Module for Place
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
import models


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['GET'])
def place_all(city_id):
    """
    Place objects listed in their entirety
    """
    city = models.storage.get(City, city_id)
    if city is None:
        abort(404)

    place_holder = []
    for place in models.storage.all(Place).values():
        if place.city_id == city.id:
            place_holder.append(place.to_dict())

    if place_holder is None:
        abort(404)

    return_holder = jsonify(place_holder)
    return return_holder


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def place_one(place_id):
    """
    Place object retrieved with 404 error handling
    when place_id is not linked to any Place object
    """
    place_one = models.storage.get(Place, place_id)
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


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False,
                 methods=['POST'])
def place_create(city_id):
    """
    Place created with specific parameters:
    - Use Flask's request.get_json to turn HTTP body request to dict
    - If HTTP body request isn't valid JSON raise error 400 w/ message
    - If dict doesn't contain key email raise error 400 w/ message
    Returns: New Place with status code 201
    """
    if models.storage.get(City, city_id) is None:
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
    request_help["city_id"] = city_id
    create_help = models.place.Place(**request_help)
    create_help.save()
    return_holder = jsonify(create_help.to_dict())
    return make_response(return_holder, 200)


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
    ignore_these = ["id", "user_id", "city_id", "created_at", "updated_at"]
    update_help = models.storage.get(Place, place_id)
    if update_help is None:
        abort(404)
    for k_ey, v_al in request_help.items():
        if k_ey not in ignore_these:
            setattr(update_help, k_ey, v_al)
        update_help.save()
        return_holder = jsonify(update_help.to_dict())
        return return_holder


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def places_search():
    """ Returns a list of places based on state, city, and/or amenity """
    request_help = request.get_json()
    if request_help is None:
        return_holder = jsonify(error="Not a JSON")
        return make_response(return_holder, 400)
    places_holder = []
    places_return = []
    if len(request_help.keys()) == 0 or\
        (("states" not in request_help or
          len(request_help["states"]) == 0) and
         ("cities" not in request_help or
          len(request_help["cities"]) == 0)):
        for place in models.storage.all(Place).values():
            places_holder.append(place)
        if "amenities" not in request_help or\
                len(request_help["amenities"]) == 0:
            for place in places_holder:
                places_return.append(place.to_dict())
            return jsonify(places_return)
    else:
        if "states" in request_help and len(request_help["states"]) != 0:
            """ Get all matching all cities in these states """
            for state_id in request_help["states"]:
                for state in models.storage.all(State).values():
                    if state.id == state_id:
                        for city in state.cities:
                            for place in models.storage.all(Place).values():
                                if place.city_id == city.id:
                                    places_holder.append(place)

        if "cities" in request_help and len(request_help["cities"]) != 0:
            """ Get all matching these cities """
            for city_id_l in request_help["cities"]:
                for city in models.storage.all(City).values():
                    if city.id == city_id_l:
                        for place in models.storage.all(Place).values():
                            if place.city_id == city.id and\
                                    place not in places_holder:
                                places_holder.append(place)

    if "amenities" in request_help and len(request_help["amenities"]) != 0:
        amenities = []
        for amenitiy_id in request_help["amenities"]:
            for amenity in models.storage.all(Amenity).values():
                if amenity.id == amenity_id:
                    amenities.append(amenity)
        for place in places_holder:
            if all(amenity in place.amenities for amenity in amenities):
                places_return.append(place.to_dict())
        return jsonify(places_return)
    else:
        for place in places_holder:
            places_return.append(place.to_dict())
        return jsonify(places_return)
