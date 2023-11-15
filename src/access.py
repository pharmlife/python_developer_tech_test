from flask import jsonify, Response
import database


def request_person_data() -> (Response, int):
    raw_data = database.get_people()
    formatted_data = _format_data(raw_data)

    return jsonify(formatted_data), 200


def add_person(name: str) -> (Response, int):
    if _name_exists(name):
        err_msg = f"Name {name} exists."
        return jsonify({"error": err_msg}), 409

    new_id = database.add_person(name)
    response = jsonify({"id": str(new_id), "name": name}), 200

    return jsonify(response), 200


def delete_person(pid: int):
    if _id_exists(pid):
        return jsonify({"error": "Not Found"}), 404

    database.delete_person(pid)

    return jsonify({}), 204


def check_status():
    active = database.get_db_status()

    if active:
        return jsonify({"msg": "Ok"}), 200

    return jsonify({"error": "Database is not active"}), 500


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
