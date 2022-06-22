import sqlite3
import os

FILENAME = "database.db"


def ensure_tables_are_created():
    """
    Initialize the database. This method should be called at least once before actually using the database.
    Can safely be called multiple times if necessary.
    """
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS person
               (id INTEGER PRIMARY KEY AUTOINCREMENT, name text NOT NULL)''')
    con.commit()
    con.close()


def get_people():
    """
    Get all the content of the database as an array of tuples (id, name).

    Return example:
        [
            (
                1,
                "Rae"
            ),
            (
                2,
                "Matt"
            )
        ]
    """
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()
    result = cur.execute("SELECT * FROM person").fetchall()
    con.close()
    return result


def add_person(name):
    """
    Add a person in the collection given a name.
    
    :param: name: The name of the new person to add
    :return: The id of the new person
    """
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()
    cur.execute("INSERT INTO person(name) VALUES(?)", [name])
    id = cur.lastrowid
    con.commit()
    con.close()
    return id


def delete_person(id):
    """
    Deletes a person by id.

    :param: id: The person id to delete
    :return: True if the person existed and has been succesfully deleted. False otherwise
    """
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()
    result = cur.execute("DELETE FROM person where id = ?", (id,))
    deleted = result.rowcount
    con.commit()
    con.close()
    return deleted == 1


def get_db_status():
    """
    Returns the status of the database. For simplicity, it only checks if the database file exists
    :return True if the database status is correct. False otherwise
    """
    return os.path.exists(FILENAME)
