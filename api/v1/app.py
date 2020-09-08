#!/usr/bin/python3
""" App """
from flask import Flask
app = Flask(__name__)
from models import storage
from api.v1.views import app_views
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ Called after each request """
    storage.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
