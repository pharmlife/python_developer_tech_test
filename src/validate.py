from flask import jsonify


def check_token(token: str):
    response = jsonify([])

    if not token:
        response = jsonify({"error": "Authorization required"})
        response.status_code = 401

    return response


def check_name_data(name_data: [{str: str}]):
    name = name_data["name"] or None

    response = jsonify([])

    if name is None or not name.isalnum():
        response = jsonify({"error": "Names must be alphanumeric"})
        response.status_code = 400

    return response

