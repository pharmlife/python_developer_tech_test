from flask import jsonify, Response
import database


def request_person_data() -> Response:
    """
    Request the person data from the database.

    :return: A flask.Response containing the data. For example -

    response.get_json() =
    [
        {
            "id": 1,
            "name": "Jane"
        },
        {
            "id": 2,
            "name": "John"
        }
    ]

    If the database is empty, response.get_json() will return an empty list.
    """
    raw_data = database.get_people()
    formatted_data = _format_data(raw_data)

    response = jsonify(formatted_data)

    return response


def check_person_name_exists(name: str) -> bool:
    """
    Check whether a name already exists in the database.

    :param name: The name of the person to check.
    :return: True if the name is found, False if not.
    """
    existing_names = _access_name_data()

    return name in existing_names


def add_person(name: str) -> Response:
    """
    Add a new person to the database. The code will first check if the person exists before adding.

    :param name: The name of the person to add.
    :return: A flask.Response containing the id and name of the new entry, and status code of 201. For example -

    response.get_json() = {"id": 1, "name": "Jane"}
    response.status_code = 201

    If the name already exists, the status code will be 409 and the data will contain an error message.
    """
    person_exists = check_person_name_exists(name)

    if person_exists:
        response = jsonify({"error": "Name exists"})
        response.status_code = 409

        return response

    new_id = database.add_person(name)
    response = jsonify({"id": new_id, "name": name})
    response.status_code = 201

    return response


def check_person_id_exists(person_id: int) -> bool:
    """
    Check whether a person_id already exists in the database.

    :param person_id: The person id to check.
    :return: True if the person id is found, False if not.
    """
    existing_ids = _access_person_id_data()

    return person_id in existing_ids


def delete_person(person_id: int) -> Response:
    """
    Delete a person from the database by providing their associated person_id. The code will first check if the
    person_id exists before trying to delete.

    :param person_id: The id associated with the person.
    :return: A flask.Response with a status code of 204 if deletion is successful. If the person_id cannot be found, the
    status code will be 404 and the data will contain an error message.
    """
    id_exists = check_person_id_exists(person_id)

    if not id_exists:
        response = jsonify({"error": "Not Found"})
        response.status_code = 404
        return response

    database.delete_person(person_id)
    response = jsonify('null')
    response.status_code = 204

    return response


def check_status() -> Response:
    """
    Check the status of the database.

    :return: a flask.Response. If active, the status code will be 200. If inactive, the status code will be 500.
    """
    active = database.get_db_status()

    if not active:
        response = jsonify({"error": "Database is not active"})
        response.status_code = 500

        return response

    response = jsonify({"msg": "Ok"})
    response.status_code = 200

    return response


def _access_name_data() -> list:
    """
    Access the names from the raw database data.

    :return: A list of names.
    """
    raw_data = database.get_people()
    names = [_[1] for _ in raw_data]

    return names


def _access_person_id_data() -> list:
    """
    Access the person ids from the raw database data.

    :return: A list of person ids.
    """
    raw_data = database.get_people()
    ids = [_[0] for _ in raw_data]

    return ids


def _format_data(raw_data: [(int, str)]) -> list:
    """
    Format raw data from SQL database into a list of dictionaries.

    :param raw_data: Raw data from the database.
    :return: A formatted list of dictionaries.
    """
    formatted = []
    for dat in raw_data:
        formatted_dat = {"id": dat[0], "name": dat[1]}
        formatted.append(formatted_dat)

    return formatted
