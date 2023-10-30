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
