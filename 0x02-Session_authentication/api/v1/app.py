#!/usr/bin/env python3
""" App """ 
import os
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import CORS

from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine the authentication method to use based on environment variable
authentication_method = getenv('AUTH_TYPE', 'auth')
auth = None

if authentication_method == 'auth':
    auth = Auth()
elif authentication_method == 'basic_auth':
    auth = BasicAuth()
elif authentication_method == 'session_auth':
    auth = SessionAuth()
elif authentication_method == 'session_exp_auth':
    auth = SessionExpAuth()
elif authentication_method == 'session_db_auth':
    auth = SessionDBAuth()


@app.errorhandler(404)
def handle_not_found(error) -> str:
    """Handle 404 errors when a resource is not found."""
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(401)
def handle_unauthorized(error) -> str:
    """Handle 401 errors when authorization is required."""
    return jsonify({"error": "Unauthorized access"}), 401


@app.errorhandler(403)
def handle_forbidden(error) -> str:
    """Handle 403 errors when access is forbidden."""
    return jsonify({"error": "Access forbidden"}), 403


@app.before_request
def verify_user_authentication():
    """Verify the user's authentication status before processing a request."""
    if auth:
        public_endpoints = [
            "/api/v1/status/",
            "/api/v1/unauthorized/",
            "/api/v1/forbidden/",
            "/api/v1/auth_session/login/",
        ]
        if auth.require_auth(request.path, public_endpoints):
            current_user = auth.current_user(request)
            if auth.authorization_header(request) is None and \
                    auth.session_cookie(request) is None:
                abort(401)
            if current_user is None:
                abort(403)
            request.current_user = current_user


if __name__ == "__main__":
    server_host = getenv("API_HOST", "0.0.0.0")
    server_port = getenv("API_PORT", "5000")
    app.run(host=server_host, port=server_port)
