from flask import Flask, request, jsonify

app = Flask(__name__)

db = [
        {
            "id": 0,
            "name": "Test Name A"
        },
        {
            "id": 1,
            "name": "Test Name B"
        }
    ]

db_active = True


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

    return jsonify(db), 200


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

    new_id = len(db) + 1
    new_name = str(data["name"])
    new_person = {"id": new_id, "name": new_name}

    db.append(new_person)

    return jsonify(new_person), 201


@app.route('/person/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    """
    Example usage:
    `curl ${SERVER}/person/${OWNER ID} -X DELETE -H 'x-api-key: ${TOKEN}'`

    """
    auth_response = authenticate_request()
    if auth_response:
        return auth_response

    ids = [_["id"] for _ in db]

    if str(person_id) not in ids:
        return jsonify({"error": "Not Found"}), 404

    return '', 204


@app.route('/status', methods=['GET'])
def get_status():
    """
    Example usage:
    `curl ${SERVER}/status`

    """
    if db_active:
        return jsonify({"msg": "Ok"}), 200

    return jsonify({"error": "Database is inactive"}), 500


if __name__ == '__main__':
    app.run(debug=True)
