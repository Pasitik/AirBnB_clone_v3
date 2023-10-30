#!/usr/bin/python3
"""api amenities"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User

import json


@app_views.route("/users", methods=["GET"])
def get_users():
    """retrieves all users"""
    allUsers = storage.all(User).values()
    userList = []
    for user in allUsers:
        userList.append(user.to_dict())
    response = make_response(json.dumps(userList), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users/<id>", methods=["GET"])
def get_user(id):
    """retrieves amenity object with id"""
    user = storage.get(User, id)
    if not user:
        abort(404)
    response_data = user.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users/<string:id>", methods=["DELETE"])
def delete_user(id):
    """delets amenity with id"""
    user = storage.get(User, id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users", methods=["POST"])
def create_user():
    """inserts user if its valid json"""

    if not request.get_json():
        abort(400, description="Not a JSON")
    if "email" not in request.get_json():
        abort(400, description='Missing email')
    if "password" not in request.get_json():
        abort(400, description='Missing password')
    data = request.get_json()
    instObj = User(**data)
    instObj.save()
    res = instObj.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users/<id>", methods=["PUT"])
def put_user(id):
    """update a users by id"""
    user = storage.get(User, id)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignoreKeys = ["id", "email", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(user, key, value)
    storage.save()
    res = user.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response
