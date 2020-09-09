#!/usr/bin/python3
"""
Module for Cities
"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
import models


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def cities_all():
    """
    """


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def cities_one(state_id):
    """
    """


@app_views.route('/states', strict_slashes=False, methods=['DELETE'])
def cities_delete(state_id):
    """
    """


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def cities_create():
    """
    """


@app_views.route('/states', strict_slashes=False, methods=['PUT'])
def cities_update(state_id):
    """
    """