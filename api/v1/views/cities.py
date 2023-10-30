#!/usr/bin/python3
"""api states"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def get_cities(state_id):
    """retrieves all city object"""
    state = storage.get(State, id_state)
    if not state:
        abort(404)
    allCities = storage.all(City).values()
    citiesList = []
    for city in allCities:
        if city.state_id == state_id:
            citiesList.append(city.to_dict())
    response = make_response(json.dumps(citiesList), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """retrieves city object with id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    response_data = city.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """delets state with id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """inserts state if its valid json amd has correct key"""
    abortMSG = "Not a JSON"
    missingMSG = "Missing name"

    state = storage.get(State, id_state)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    if "name" not in request.get_json():
        abort(400, description=missingMSG)
    data = request.get_json()
    data["state_id"] = state_id
    instObj = City(**data)
    instObj.save()
    res = instObj.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<city_id>", methods=["PUT"])
def put_city(city_id):
    """update a state by id"""
    abortMSG = "Not a JSON"
    city = storage.get(City, city_id)
    ignoreKeys = ["id", "created_at", "updated_at"]
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(city, key, value)
    storage.save()
    res = city.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response
