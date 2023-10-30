#!/usr/bin/python3
"""api states"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.state import Amenity
import json


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """retrieves all Amenity object"""
    allAmenities = storage.all(Amenity).values()
    amaenityList = []
    for amenity in allAmenities:
        amenityList.append(amenity.to_dict())
    response = make_response(json.dumps(amenityList), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
def get_amenity(amenity_id):
    """retrieves Amenity object with id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    response_data = amenity.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """delets amenity with id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """inserts state if its valid json amd has correct key"""
    abortMSG = "Not a JSON"
    missingMSG = "Missing name"
    if not request.get_json():
        abort(400, description=abortMSG)
    if "name" not in request.get_json():
        abort(400, description=missingMSG)
    data = request.get_json()
    instObj = Amenity(**data)
    instObj.save()
    res = instObj.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """update a state by id"""
    abortMSG = "Not a JSON"
    amenity = storage.get(Amenity, amenity_id)
    ignoreKeys = ["id", "created_at", "updated_at"]
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(amenity, key, value)
    storage.save()
    res = amenity.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response
