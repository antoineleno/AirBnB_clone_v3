#!/usr/bin/python3
"""
API module
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"api/v1/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Return a JSON response for 404 errors."""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=int(port), threaded=True)
