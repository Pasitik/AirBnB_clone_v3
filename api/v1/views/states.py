#!/usr/bin/python3
from flask import request, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def get_sates():
    """get states"""
    all_states = storage.all(State).values()
    states_list = list(map(lambda x: x.to_dict(), all_states))
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id=None):
    """get state by id"""
    all_states = storage.all(State).values()
    state = list(filter(lambda x: x.id == state_id, all_states))
    if state:
        return jsonify(state[0].to_dict())
    abort(404)


@app_views.route('/state/<state_id>', methods=['DELETE'])
def del_state(state_id):
    """delete a state"""
    all_states = storage.all(State).values()
    state = list(filter(lambda x: x.id == state.id, all_states))
    if state:
        storage.delete(state[0])
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/states/', methods=['POST'])
def add_state():
    """creates a state"""
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def updates_state(state_id):
    '''Updates a State object'''
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
