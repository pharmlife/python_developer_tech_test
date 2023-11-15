from flask import Flask, request
import access as database_access
import validate

app = Flask(__name__)


@app.route('/person', methods=['GET'])
def get_persons():
    """
    Example usage:
    `curl ${SERVER}/person -H 'x-api-key: ${TOKEN}'`

    """
    token_error = _validate_request_token()
    if token_error:
        return token_error

    response, code = database_access.request_person_data()

    return response, code


@app.route('/person', methods=['POST'])
def create_person():
    """
    Example usage:
    `curl ${SERVER}/person -H 'x-api-key: ${TOKEN}' -H 'Content-Type: application/json' -d '{"name": ${NAME} }'`

    """
    token_error = _validate_request_token()
    if token_error:
        return token_error

    data_error = _validate_user_data()
    if data_error:
        return data_error

    name = request.get_json()["name"]
    response, code = database_access.add_person(name)

    return response, code


@app.route('/person/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    """
    Example usage:
    `curl ${SERVER}/person/${OWNER ID} -X DELETE -H 'x-api-key: ${TOKEN}'`

    """
    token_error = _validate_request_token()
    if token_error:
        return token_error

    response, code = database_access.delete_person(person_id)

    return response, code


@app.route('/status', methods=['GET'])
def get_status():
    """
    Example usage:
    `curl ${SERVER}/status`

    """
    response, code = database_access.check_status()

    return response, code


def _validate_request_token():
    token = request.headers.get("x-api-key")
    response, code = validate.check_token(token)

    if code != 200:
        return response, code


def _validate_user_data():
    name_data = request.get_json()
    response, code = validate.check_name_data(name_data)

    if code != 200:
        return response, code


if __name__ == '__main__':
    app.run(debug=True)
