from flask import Flask, request, jsonify
import access as database_access

app = Flask(__name__)


def authenticate_request():
    token = request.headers.get("x-api-key")
    if not token:
        return jsonify({"error": "Authorization required"}), 401


@app.route('/person', methods=['GET'])
def get_persons():
    """
    Example usage:
    `curl ${SERVER}/person -H 'x-api-key: ${TOKEN}'`

    """
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

    response, code = database_access.request_person_data()

    return response, code


@app.route('/person', methods=['POST'])
def create_person():
    """
    Example usage:
    `curl ${SERVER}/person -H 'x-api-key: ${TOKEN}' -H 'Content-Type: application/json' -d '{"name": ${NAME} }'`

    """
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

    content_type = request.headers.get("Content-Type")
    if content_type != "application/json":
        return jsonify({"error": "Invalid Content-Type"}), 400

    data = request.get_json()
    if not data["name"].isalnum():
        return jsonify({"error": "Names must be alphanumeric"}), 400

    response, code = database_access.add_person(data["name"])

    return response, code


@app.route('/person/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    """
    Example usage:
    `curl ${SERVER}/person/${OWNER ID} -X DELETE -H 'x-api-key: ${TOKEN}'`

    """
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

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


if __name__ == '__main__':
    app.run(debug=True)
