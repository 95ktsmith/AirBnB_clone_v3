#!/usr/bin/python3
""" App """
from models import storage
from flask import Flask, jsonify
from os import getenv
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ Called after each request """
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ Page not found """
    return jsonify({"error": "Not found"})

if __name__ == "__main__":
    if getenv('HBNB_API_HOST') is None:
        host = '0.0.0.0'
    else:
        host = getenv('HBNB_API_HOST')

    if getenv('HBNB_API_PORT') is None:
        port = '5000'
    else:
        port = getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
