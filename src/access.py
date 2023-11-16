from flask import jsonify, Response
import database


def request_person_data() -> (Response, int):
    raw_data = database.get_people()
    formatted_data = _format_data(raw_data)

    response = jsonify(formatted_data)

    return response


def add_person(name: str) -> (Response, int):
    if _name_exists(name):
        err_msg = f"Name {name} exists."
        response = jsonify({"error": err_msg})
        response.status_code = 409

        return response

    new_id = database.add_person(name)
    response = jsonify({"id": str(new_id), "name": name})
    response.status_code = 201

    return response


def delete_person(pid: int):
    if not _id_exists(pid):
        response = jsonify({"error": "Not Found"})
        response.status_code = 404
        return response

    database.delete_person(pid)

    response = jsonify('null')
    response.status_code = 204

    return response


def check_status():
    active = database.get_db_status()

    if not active:
        response = jsonify({"error": "Database is not active"})
        response.status_code = 500

        return response

    response = jsonify({"msg": "Ok"})
    response.status_code = 200

    return response


def _access_name_data():
    raw_data = database.get_people()
    names = [_[1] for _ in raw_data]

    return names


def _access_id_data():
    raw_data = database.get_people()
    ids = [_[0] for _ in raw_data]

    return ids


def _name_exists(name: str):
    names = _access_name_data()

    return name in names


def _id_exists(id: int):
    ids = _access_id_data()

    return id in ids


def _format_data(raw_data: [(int, str)]) -> [{str: str}]:
    formatted = []
    for dat in raw_data:
        formatted_dat = {"id": str(dat[0]), "name": dat[1]}
        formatted.append(formatted_dat)

    return formatted


def _unformat_data(formatted_data: [{str: str}]) -> [(int, str)]:
    raw = []

    for dat in formatted_data:
        raw_dat = [int(dat[id]), dat["name"]]
        raw.append(raw_dat)

    return raw
