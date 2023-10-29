#!/usr/bin/python3
from fask import request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', method=['GET'])
def get_sates():
    all_states = storage.all(State).values()
	states_list = list(map(lambda x: x.to_dict(), all_states))
	return jsonify(states_list)

@app_views.route('/states/<state_id>', method=['GET'])
def get_state():
    all_states = storage.all(State).values()
    state = list(filter(lambda x: x.id == state_id, all_states))
	return jsonify(state[0].to_dict())
    



