#!/usr/bin/python3
"""
Contains the TestStateDocs classes
"""
import os
import json
import tempfile
import unittest
from models import storage
from api.v1.app import app
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review


class TestClient(unittest.TestCase):
    """ Test places endpoint"""

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True

        self.client = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_get_places(self):
        """ Test places endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        new_city = City(name="Apollonia", state_id=new_state.id)
        storage.new(new_city)
        storage.save()
        new_amenity = Amenity(name="wifi")
        storage.new(new_amenity)
        storage.save()
        new_user = User(
                first_name="Jane", last_name="Doe",
                email="jdoe@test.com", password="password"
            )
        storage.new(new_user)
        storage.save()
        new_place = Place(
                city_id=new_city.id,
                user_id=new_user.id,
                name="Achimota",
                description="",
                number_rooms=3,
                number_bathrooms=4,
                max_guest=6,
                price_by_night=19,
                latitude=0.045,
                longitude=0.067,
                amenity_ids=[new_amenity.id]
            )
        storage.new(new_place)
        storage.save()

        rv = self.client.get(f'/api/v1/cities/{new_city.id}/places')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data[0].get('__class__') == "Place"

    def test_get_a_placesa_reviews(self):
        """test_get_a_places_reviews"""
        new_state = State(name="AccVra")
        storage.new(new_state)
        storage.save()
        new_city = City(name="Apollonia", state_id=new_state.id)
        storage.new(new_city)
        storage.save()
        new_amenity = AASmenity(name="wifi")
        storage.new(new_amenity)
        storage.save()
        new_user = User(
                first_name="Jane", last_name="Doe",
                email="jdoe@test.com", password="password"
            )
        storage.new(new_user)
        storage.save()
        new_place = Place(
                city_id=new_city.id,
                user_id=new_user.id,
                name="Achimota",
                description="",
                number_rooms=3,
                number_bathrooms=4,
                max_guest=6,
                price_by_night=19,
                latitude=0.045,
                longitude=0.067,
                amenity_ids=[new_amenity.id]
            )
        storage.new(new_place)
        storage.save()

        rv = self.client.get(f'api/v1/places/{new_place.id}')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data.get('__class__') == "Review"

    def test_delete_a_places(self):
        """ Test places endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        new_city = City(name="Apollonia", state_id=new_state.id)
        storage.new(new_city)
        storage.save()
        new_amenity = Amenity(name="wifi")
        storage.new(new_amenity)
        storage.save()
        new_user = User(
                first_name="Jane", last_name="Doe",
                email="jdoe@test.com", password="password"
            )
        storage.new(new_user)
        storage.save()
        new_place = Place(
                city_id=new_city.id,
                user_id=new_user.id,
                name="Achimota",
                description="",
                number_rooms=3,
                number_bathrooms=4,
                max_guest=6,
                price_by_night=19,
                latitude=0.045,
                longitude=0.067,
                amenity_ids=[new_amenity.id]
            )
        storage.new(new_place)
        storage.save()

        rv = self.client.delete(f'/api/v1/places/{new_place.id}')
        assert b'{}' in rv.data

        rv = self.client.delete(f'/api/v1/places/{new_user.id}')
        data = json.loads(rv.data)
        assert 'Not found' == data.get('error')
        assert 'error' in data
        assert rv.status_code == 404

    def test_create_a_places_reviews(self):
        """ Test places endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        new_city = City(name="Apollonia", state_id=new_state.id)
        storage.new(new_city)
        storage.save()
        new_amenity = Amenity(name="wifi")
        storage.new(new_amenity)
        storage.save()
        new_user = User(
                first_name="Jane", last_name="Doe",
                email="jdoe@test.com", password="password"
            )
        storage.new(new_user)
        storage.save()
        new_place = Place(
                city_id=new_city.id,
                user_id=new_user.id,
                name="Achimota",
                description="",
                number_rooms=3,
                number_bathrooms=4,
                max_guest=6,
                price_by_night=19,
                latitude=0.045,
                longitude=0.067,
                amenity_ids=[new_amenity.id]
            )
        storage.new(new_place)
        storage.save()

        body = {
                    "name": "Lapaz",
                    "description": "",
                    "number_rooms": 3,
                    "number_bathrooms": 4,
                    "max_guest": 6,
                    "price_by_night": 19,
                    "user_id": new_user.id
		}

        rv = self.client.post(f'/api/v1/cities/{new_city.id}/places', json=body)
        assert json.loads(rv.data).get('name') == body.get('name')
        assert rv.status_code == 201

    def test_edit_a_places_reviews(self):
        """ Test places endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        new_city = City(name="Apollonia", state_id=new_state.id)
        storage.new(new_city)
        storage.save()
        new_amenity = Amenity(name="wifi")
        storage.new(new_amenity)
        storage.save()
        new_user = User(
                first_name="Jane", last_name="Doe",
                email="jdoe@test.com", password="password"
            )
        storage.new(new_user)
        storage.save()
        new_place = Place(
                city_id=new_city.id,
                user_id=new_user.id,
                name="Achimota",
                description="",
                number_rooms=3,
                number_bathrooms=4,
                max_guest=6,
                price_by_night=19,
                latitude=0.045,
                longitude=0.067,
                amenity_ids=[new_amenity.id]
            )
        storage.new(new_place)
        storage.save()

        new_review = Review(
                place_id=new_place.id,
                user_id=new_user.id,
                text="A nice place to be"
        )
        storage.new(new_review)
        storage.save()
        
        
        body = {
                    "name": "Lapaz",
                    "description": "",
                    "number_rooms": 3,
                    "number_bathrooms": 4,
                    "max_guest": 6,
                    "price_by_night": 19,
		}
        rv = self.client.put(f'/api/v1/places/{new_place.id}', json=body)
        assert json.loads(rv.data).get('text') == body.get('text')
        assert rv.status_code == 200


    if __name__ == '__main__':
        unittest.main()
