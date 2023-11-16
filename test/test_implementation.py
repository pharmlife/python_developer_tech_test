import pytest

import database
from app import app
import json


@pytest.fixture
def set_up_database():
    import database
    import os

    if os.path.exists("database.db"):
        os.remove("database.db")

    database.ensure_tables_are_created()
    database.add_person("TestPerson")

    yield


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_get_persons(client, set_up_database):
    response = client.get('/person', headers={'x-api-key': 'token'})
    data = response.get_json()

    assert response.status_code == 200
    assert data == [{'id': 1, 'name': 'TestPerson'}]


def test_get_persons_without_token(client, set_up_database):
    response = client.get('/person')
    data = response.get_json()

    assert response.status_code == 401
    assert data == {"error": "Authorization required"}


def test_create_person(client, set_up_database):
    new_person_data = {"name": "NewPerson"}
    new_person_data = json.dumps(new_person_data)

    response = client.post('/person', headers={'x-api-key': 'valid_token_1'},
                           content_type='application/json', data=new_person_data)
    data = response.get_json()

    assert response.status_code == 201
    assert data == {'id': '2', 'name': 'NewPerson'}

    people = database.get_people()
    assert len(people) == 2


def test_create_person_without_token(client, set_up_database):
    new_person_data = {"name": "NewPerson"}
    new_person_data = json.dumps(new_person_data)

    response = client.post('/person', content_type='application/json', data=new_person_data)
    data = response.get_json()

    assert response.status_code == 401
    assert data == {"error": "Authorization required"}

    people = database.get_people()
    assert len(people) == 1


def test_create_person_with_non_alphanumeric_name(client, set_up_database):
    new_person_data = {"name": "&^$£@"}
    new_person_data = json.dumps(new_person_data)

    response = client.post('/person', headers={'x-api-key': 'valid_token_1'},
                           content_type='application/json', data=new_person_data)
    data = response.get_json()

    assert response.status_code == 400
    assert data == {"error": "Names must be alphanumeric"}

    people = database.get_people()
    assert len(people) == 1


def test_delete_person(client, set_up_database):
    client = app.test_client()
    response = client.delete('/person/1', headers={'x-api-key': 'valid_token_1'})

    assert response.data == b''
    assert response.status_code == 204

    people = database.get_people()
    assert len(people) == 0


def test_delete_person_without_token(client, set_up_database):
    response = client.delete('/person/1')
    data = response.get_json()

    assert response.status_code == 401
    assert data == {"error": "Authorization required"}

    people = database.get_people()
    assert len(people) == 1


def test_delete_person_not_found(client, set_up_database):
    response = client.delete('/person/999', headers={'x-api-key': 'valid_token_1'})
    data = response.get_json()

    assert data == {"error": "Not Found"}
    assert response.status_code == 404


def test_status_database_exists(client, set_up_database):
    response = client.get('/status')
    data = response.get_json()

    assert data == {"msg": "Ok"}
    assert response.status_code == 200


def test_status_database_does_not_exist(client):
    import os

    if os.path.exists("database.db"):
        os.remove("database.db")

    response = client.get('/status')
    data = response.get_json()

    assert data == {"error": "Database is not active"}
    assert response.status_code == 500
