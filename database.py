import sqlite3

FILENAME = "database.db"


def ensure_tables_are_created():
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS person
               (id INTEGER PRIMARY KEY AUTOINCREMENT, name text NOT NULL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS person_alias (id INTEGER PRIMARY KEY AUTOINCREMENT, alias text NOT 
    NULL, person_id INTEGER NOT NULL, FOREIGN KEY (person_id) REFERENCES people(id))''')

    con.commit()
    con.close()


def get_people():
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()
    result = cur.execute("SELECT * FROM person").fetchall()
    con.close()
    return result


def add_person(name):
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()
    cur.execute("INSERT INTO person(name) VALUES(?)", [name])
    id = cur.lastrowid
    con.commit()
    con.close()
    return id


def delete_person(id):
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()
    result = cur.execute("DELETE FROM person where id = ?", (id))
    deleted = result.rowcount
    con.commit()
    con.close()
    return deleted == 1


def get_alias(person_id):
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()
    result = cur.execute("SELECT alias FROM person_alias WHERE person_id = ?", (person_id)).fetchall()
    con.close()
    return result


def add_alias(person_id, alias):
    con = sqlite3.connect(FILENAME)
    cur = con.cursor()
    cur.execute("INSERT INTO person_alias(person_id, alias) VALUES(?, ?)", (person_id, alias)).fetchall()
    con.commit()
    con.close()


def get_db_status():
    # It's always running perfectly :)
    return True
