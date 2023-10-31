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
    """Tests to check the documentation and style of State class"""
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True

        self.client = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_ping(self):
        """Start with a blank database."""

        rv = self.client.get('/api/v1/status')
        assert b'OK' in rv.data
        assert 'application/json' in rv.headers.get('Content-Type', b'')

    def test_stats(self):
        """Test stat endpoint."""

        rv = self.client.get('/api/v1/stats')
        data = json.loads(rv.data)
        assert data.get('states') == storage.count(State)

    def test_not_found(self):
        """ Test not found"""
        rv = self.client.get('/api/v1/nop')
        data = json.loads(rv.data)
        assert 'Not found' == data.get('error')
        assert 'error' in data

    def test_get_all_states(self):
        """ Test states endpoint"""
        rv = self.client.get('/api/v1/states')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data[0].get("__class__") == "State"

    def test_get_a_single_state(self):
        """ Test states endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        rv = self.client.get(f'/api/v1/states/{new_state.id}')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data.get('__class__') == "State"
        rv = self.client.get(f'/api/v1/states/{new_state.id}1')
        data = json.loads(rv.data)
        assert 'Not found' == data.get('error')
        assert 'error' in data
        assert rv.status_code == 404

    def test_delete_a_single_state(self):
        """ Test states endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        rv = self.client.delete(f'/api/v1/states/{new_state.id}')
        assert b'{}' in rv.data

    def test_post_a_single_state(self):
        """ Test states endpoint"""
        new_state = {"name": "Accra"}
        rv = self.client.post('/api/v1/states', json=new_state)
        assert rv.status_code == 201

    def test_put_a_single_state(self):
        """ Test states endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        body = {"name": "Tema"}
        rv = self.client.put(
                f'/api/v1/states/{new_state.id}', json=body
            )
        data = json.loads(rv.data)
        assert rv.status_code == 200
        body = json.dumps(body)
        assert data.get('name') in body

    def test_get_cities_of_state(self):
        """ Test states endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        new_city = City(name="Apollonia", state_id=new_state.id)
        storage.new(new_city)
        storage.save()
        rv = self.client.get(f'/api/v1/states/{new_state.id}/cities')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data[0].get('__class__') == "City"
        assert data[0].get('id') == new_city.id
        rv = self.client.get(f'/api/v1/states/{new_state.id}1')
        data = json.loads(rv.data)
        assert 'Not found' == data.get('error')
        assert 'error' in data
        assert rv.status_code == 404

    def test_get_a_single_city(self):
        """ Test states endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        new_city = City(name="Apollonia", state_id=new_state.id)
        storage.new(new_city)
        storage.save()
        rv = self.client.get(f'/api/v1/cities/{new_city.id}')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data.get('__class__') == "City"
        assert data.get('id') == new_city.id
        rv = self.client.get(f'/api/v1/states/{new_state.id}1')
        data = json.loads(rv.data)
        assert 'Not found' == data.get('error')
        assert 'error' in data
        assert rv.status_code == 404

    def test_deletes_a_single_city(self):
        """ Test states endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        new_city = City(name="Apollonia", state_id=new_state.id)
        storage.new(new_city)
        storage.save()
        rv = self.client.delete(f'/api/v1/cities/{new_city.id}')
        assert b'{}' in rv.data

        rv = self.client.get(f'/api/v1/cities/{new_state.id}')
        data = json.loads(rv.data)
        assert 'Not found' == data.get('error')
        assert 'error' in data
        assert rv.status_code == 404

    def test_post_a_single_city(self):
        """ Test states endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        body = {'name': "Apollonia"}
        rv = self.client.post(
                f'/api/v1/states/{new_state.id}/cities', json=body
            )

        assert json.loads(rv.data).get('name') == body.get('name')
        assert rv.status_code == 201

    def test_put_a_single_city(self):
        """ Test states endpoint"""
        new_state = State(name="Accra")
        storage.new(new_state)
        storage.save()
        new_city = City(name="Apollonia", state_id=new_state.id)
        storage.new(new_city)
        storage.save()
        body = {"name": "Atadeka"}
        rv = self.client.put(f'/api/v1/cities/{new_city.id}', json=body)
        assert json.loads(rv.data).get('name') == body.get('name')
        assert rv.status_code == 200

    def test_get_amenities(self):
        """ Test states endpoint"""
        new_amenity = Amenity(name="wifi")
        storage.new(new_amenity)
        storage.save()

        rv = self.client.get('/api/v1/amenities')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data[0].get('__class__') == "Amenity"

    def test_get_an_amenity(self):
        """ Test states endpoint"""
        new_amenity = Amenity(name="wifi")
        storage.new(new_amenity)
        storage.save()

        rv = self.client.get(f'/api/v1/amenities/{new_amenity.id}')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data.get('__class__') == "Amenity"

        rv = self.client.get(f'/api/v1/amenities/{new_amenity.id}1')
        data = json.loads(rv.data)
        assert 'Not found' == data.get('error')
        assert 'error' in data
        assert rv.status_code == 404

    def test_deletes_amenity(self):
        """ Test states endpoint"""

        new_amenity = Amenity(name="wifi")
        storage.new(new_amenity)
        storage.save()
        rv = self.client.delete(f'/api/v1/amenities/{new_amenity.id}')
        assert b'{}' in rv.data

        rv = self.client.delete(f'/api/v1/amenities/{new_amenity.id}1')
        data = json.loads(rv.data)
        assert 'Not found' == data.get('error')
        assert 'error' in data
        assert rv.status_code == 404

    def test_post_amenity(self):
        """ Test states endpoint"""
        body = {"name": "wifi"}

        rv = self.client.post(f'/api/v1/amenities', json=body)
        assert json.loads(rv.data).get('name') == body.get('name')
        assert rv.status_code == 201

    def test_put_a_single_amenity(self):
        """ Test states endpoint"""
        new_amenity = Amenity(name="Wifi")
        storage.new(new_amenity)
        storage.save()

        body = {"name": "Hospital"}
        rv = self.client.put(f'/api/v1/amenities/{new_amenity.id}', json=body)
        assert json.loads(rv.data).get('name') == body.get('name')
        assert rv.status_code == 200

    def test_get_users(self):
        """ Test states endpoint"""
        new_user = User(
                first_name="Jane", last_name="Doe",
                email="jdoe@test.com", password="password"
            )
        storage.new(new_user)
        storage.save()

        rv = self.client.get('/api/v1/users')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data[0].get('__class__') == "User"

    def test_get_a_user(self):
        """ Test user endpoint"""
        new_user = User(
                first_name="Jane", last_name="Doe",
                email="jdoe@test.com", password="password"
            )
        storage.new(new_user)
        storage.save()

        rv = self.client.get(f'/api/v1/users/{new_user.id}')
        data = json.loads(rv.data)
        assert len(data) > 0
        assert data.get('__class__') == "User"

    def test_deletes_user(self):
        """ Test states endpoint"""
        new_user = User(
                first_name="Jane", last_name="Doe",
                email="jdoe@test.com", password="password"
            )
        storage.new(new_user)
        storage.save()
        rv = self.client.delete(f'/api/v1/users/{new_user.id}')
        assert b'{}' in rv.data

        rv = self.client.delete(f'/api/v1/users/{new_user.id}1')
        data = json.loads(rv.data)
        assert 'Not found' == data.get('error')
        assert 'error' in data
        assert rv.status_code == 404

    def test_post_user(self):
        """ Test user endpoint"""
        body = {
                "first_name": "Jane", "last_name": "Doe",
                "email": "jdoe@test.com", "password": "password"
        }

        rv = self.client.post(f'/api/v1/users', json=body)
        assert json.loads(rv.data).get('name') == body.get('name')
        assert rv.status_code == 201

    def test_put_a_single_user(self):
        """ Test states endpoint"""
        new_user = User(
                first_name="Jane", last_name="Doe",
                email="jdoe@test.com", password="password"
            )
        storage.new(new_user)
        storage.save()

        body = {
                "first_name": "John", "last_name": "Doe",
                "email": "johndoe@test.com", "password": "password"
        }

        rv = self.client.put(f'/api/v1/users/{new_user.id}', json=body)
        assert json.loads(rv.data).get('first_name') == body.get('first_name')
        assert rv.status_code == 200


if __name__ == '__main__':
    unittest.main()
