from flask import jsonify


def check_token(token: str):
    if not token:
        return jsonify({"error": "Authorization required"}), 401

    return jsonify({}), 200


def check_name_data(name_data: {str: str}):
    name = name_data["name"] or None

    if name is None or not name.isalnum():
        return jsonify({"error": "Names must be alphanumeric"}), 400

