#!/usr/bin/env python3
"""Module for user-related views in the API.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users() -> str:
    """GET /api/v1/users
    Returns:
      - JSON list of all User objects.
    """
    users = [user.to_json() for user in User.all()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id
    Path parameter:
      - User ID.
    Returns:
      - JSON representation of the User object.
      - 404 if the User ID is not found.
    """
    if user_id is None:
        abort(404)
    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def remove_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id
    Path parameter:
      - User ID.
    Returns:
      - Empty JSON if the User has been successfully deleted.
      - 404 if the User ID is not found.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user() -> str:
    """POST /api/v1/users/
    JSON body:
      - email.
      - password.
      - last_name (optional).
      - first_name (optional).
    Returns:
      - JSON representation of the newly created User object.
      - 400 if user creation fails due to missing information.
    """
    request_json = None
    error_message = None
    try:
        request_json = request.get_json()
    except Exception as e:
        request_json = None
    if request_json is None:
        error_message = "Invalid JSON format"
    if error_message is None and not request_json.get("email"):
        error_message = "Email is required"
    if error_message is None and not request_json.get("password"):
        error_message = "Password is required"
    if error_message is None:
        try:
            new_user = User()
            new_user.email = request_json.get("email")
            new_user.password = request_json.get("password")
            new_user.first_name = request_json.get("first_name")
            new_user.last_name = request_json.get("last_name")
            new_user.save()
            return jsonify(new_user.to_json()), 201
        except Exception as e:
            error_message = f"User creation failed: {e}"
    return jsonify({'error': error_message}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def modify_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id
    Path parameter:
      - User ID.
    JSON body:
      - last_name (optional).
      - first_name (optional).
    Returns:
      - JSON representation of the updated User object.
      - 404 if the User ID is not found.
      - 400 if the update fails due to invalid JSON format.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    request_json = None
    try:
        request_json = request.get_json()
    except Exception as e:
        request_json = None
    if request_json is None:
        return jsonify({'error': "Invalid JSON format"}), 400
    if request_json.get('first_name') is not None:
        user.first_name = request_json.get('first_name')
    if request_json.get('last_name') is not None:
        user.last_name = request_json.get('last_name')
    user.save()
    return jsonify(user.to_json()), 200
