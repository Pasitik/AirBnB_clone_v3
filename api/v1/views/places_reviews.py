#!/usr/bin/python3
"""api reviews"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
import json


@app_views.route("/places/<string:place_id>/reviews", methods=["GET"])
def get_reviews(place_id):
    """retrieves all reviews object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    allReviews = storage.all(Review).values()
    reviewsList = []
    for review in allReviews:
        if place_id == review.place_id:
            reviewsList.append(review.to_dict())
    response = make_response(json.dumps(reviewsList), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """retrieves review object with id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    response_data = review.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(review_id):
    """delets review with id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/places/<string:place_id>/reviews", methods=["POST"])
def create_review(place_id):
    """inserts review if its valid json amd has correct key"""
    abortMSG = "Not a JSON"

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    body = request.get_json()
    if "text" not in body:
        abort(400, description="Missing text")
    if "user_id" not in body:
        abort(400, description="Missing user_id")
    user = storage.get(User, body.get('user_id'))
    if not user:
        abort(404)
    data = request.get_json()
    data['place_id'] = place_id
    instObj = Review(**data)
    storage.new(instObj)
    storage.save()
    res = instObj.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/reviews/<review_id>", methods=["PUT"])
def put_review(review_id):
    """update a review by id"""
    abortMSG = "Not a JSON"
    review = storage.get(Review, review_id)
    ignoreKeys = ["id", "created_at", "updated_at", "user_id", "place_id"]
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description=abortMSG)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(review, key, value)
    storage.save()
    res = review.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response
