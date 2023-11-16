from typing import Optional
from flask import jsonify, request, Response


def try_read_token() -> Optional[str]:
    """
    Try and read the token data from the current flask.Request.

    :return: A string containing the token data if it is read successfully. Otherwise, None.

    """
    return request.headers.get("x-api-key") or None


def try_read_name() -> Optional[str]:
    """
    Try and read the token data from the current flask.Request.

    :return: A string containing the name data if it is read successfully. Otherwise, None.

    """
    return request.get_json()["name"] or None


def check_token_valid() -> Response:
    """
    Check whether the token associated with a user request is valid.
    :return: A flask.Response. If the token is valid the status_code will be 200. Otherwise, it will be 401.

    """
    response = jsonify([])
    token = try_read_token()

    if not token:
        response = jsonify({"error": "Authorization required"})
        response.status_code = 401

    return response


def check_name_valid():
    """
    Check whether the name data associated with a user request is valid.
    :return: A flask.Response. If the name data is valid the status_code will be 200. Otherwise, it will be 400.

    """
    response = jsonify([])

    person_data = request.get_json()
    name_ok = "name" in person_data and person_data["name"].isalnum()

    if not name_ok:
        response = jsonify({"error": "Names must be alphanumeric"})
        response.status_code = 400

    return response
