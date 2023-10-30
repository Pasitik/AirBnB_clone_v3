#!/usr/bin/python3
'''Contains a Flask web application API.
'''
from flask import Flask, jsonify
import os
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.url_map.strict_slashes = False

app.register_blueprint(app_views)
cors = CORS(
    app,
    resources={r"/*": {"origins": "0.0.0.0"}}
    )


@app.errorhandler(404)
def not_found(error):
    '''Handles the 404 HTTP error code.'''
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_flask(exception):
    '''The Flask app/request context end event listener.'''
    # print(exception)
    storage.close()


if __name__ == "__main__":
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
