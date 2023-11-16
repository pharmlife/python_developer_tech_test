from flask import Flask, request, Response
import database
import access as database_access
import input


database.ensure_tables_are_created()
app = Flask(__name__)


@app.route('/person', methods=['GET'])
def get_persons() -> Response:
    """
    Request a list of persons from the database.

    :return: A flask.Response indicating if the request was successful.

    Example usage:
    `curl ${SERVER}/person -H 'x-api-key: ${TOKEN}'`

    """
    token_response = input.check_token_valid()
    if token_response.status_code != 200:
        return token_response

    response = database_access.request_person_data()

    return response


@app.route('/person', methods=['POST'])
def create_person() -> Response:
    """
    Add a person to the database. Will fail if the name data already exists.

    :return: A flask.Response indicating if the request was successful.

    Example usage:
    `curl ${SERVER}/person -H 'x-api-key: ${TOKEN}' -H 'Content-Type: application/json' -d '{"name": ${NAME} }'`

    """
    token_response = input.check_token_valid()
    if token_response.status_code != 200:
        return token_response

    name_response = input.check_name_valid()
    if name_response.status_code != 200:
        return name_response

    name = input.try_read_name()
    response = database_access.add_person(name)

    return response


@app.route('/person/<int:person_id>', methods=['DELETE'])
def delete_person(person_id: int) -> Response:
    """
    Delete a person from the database by person id (pid). Will fail if the provided pid does not already exist.

    :return: A flask.Response indicating if the request was successful.

    Example usage:
    `curl ${SERVER}/person/${OWNER ID} -X DELETE -H 'x-api-key: ${TOKEN}'`

    """
    token_response = input.check_token_valid()
    if token_response.status_code != 200:
        return token_response

    response = database_access.delete_person(person_id)

    return response


@app.route('/status', methods=['GET'])
def get_status() -> Response:
    """
    Request the status of the database.

    :return: A flask.Response indicating whether the database is active.

    Example usage:
    `curl ${SERVER}/status`

    """
    response = database_access.check_status()

    return response


if __name__ == '__main__':
    app.run(debug=True)
