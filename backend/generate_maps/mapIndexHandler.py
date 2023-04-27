"""
This module contains methods to assist with handling the MySQL Database table
named Map.

Map contains the following attributes:
    "id": string representing a base-64 unique identifier for a given map.
    "title": string representing the user-created name for a given map.
    "location": string representing a list of 2 floats specifying the
        coordinate location for the specified city
    "bounds": string representing a list of 4 floats specifying the coordinate
        bounds for the specified city

Each row in Map corresponds to a file in the /maps directory. The file name for
any corresponding map is id.json.

Global Variables:
    MAP_ID_LENGTH: length of the base-64 string for map_index attribute "id"
    MAP_ID_RETRY_LIMIT: retry limit for creating map_index attribute "id"

Functions:
    get_index: returns a list of dictionaries containing contents of Map
    create_index: creates a unique base-64 map id and entry in map_index.json
    delete_index: deletes an entry from Map and its corresponding file
    update_index: updates an entry from Map for attribute "title"

When invoked directly, the following input values can be used to call
delete_index and update_index:

Input Values:
    mode: string specifying "GET", "DELETE" or "UPDATE"
    map_id: string representing the base-64 unique identifier for the given map
    new_title: string specifying the new value for attribute "title"
"""
from json import dumps, loads
from os import remove
from os.path import dirname
from secrets import token_urlsafe
import mysql.connector


MAP_ID_LENGTH = 10 * 3//4   # multiply length by 3/4 due to Base64 encoding
MAP_ID_RETRY_LIMIT = 10000
FILE_PATH = dirname(__file__)


def retrieve_secrets():
    with open(f'{FILE_PATH}\secrets.json', 'r') as secrets:
        secrets = loads(secrets.read())
        host = secrets['DB_HOST']
        user = secrets['DB_USER']
        passwd = secrets['DB_PASSWD']
        name = secrets['DB_NAME']
    return host, user, passwd, name


def get_index():
    host, user, passwd, name, = retrieve_secrets()
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=name
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Map")
    results = cursor.fetchall()
    for result in results:
        result["location"] = loads(result["location"])
        result["bounds"] = loads(result["bounds"])
    cursor.close()
    return dumps(results)


def create_index(map_title, location, bounds):
    host, user, passwd, name, = retrieve_secrets()
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=name
    )
    cursor = db.cursor()
    cursor.execute("SELECT id FROM Map")
    results = cursor.fetchall()
    covered_names = set(result[0] for result in results)

    new_id = token_urlsafe(MAP_ID_LENGTH)
    iterations = 0
    while new_id in covered_names:
        new_id = token_urlsafe(MAP_ID_LENGTH)
        iterations += 1
        if iterations >= MAP_ID_RETRY_LIMIT:
            raise ValueError("Map ID creation failed")

    insert = (
        new_id,
        map_title,
        str(location),
        str(bounds)
    )
    cursor.execute(
        f"INSERT INTO Map (id, title, location, bounds) VALUES {insert}")
    db.commit()
    cursor.close()
    return new_id


def delete_index(map_id):
    host, user, passwd, name, = retrieve_secrets()
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=name
    )
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM Map WHERE id='{map_id}'")
    db.commit()
    cursor.close()

    try:
        remove(f'{FILE_PATH}\maps\{map_id}.json')
    except OSError:
        pass


def update_index(map_id, new_title):
    if not new_title:
        raise ValueError("Invalid new title")

    host, user, passwd, name, = retrieve_secrets()
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=name
    )
    cursor = db.cursor()
    cursor.execute(f"UPDATE Map SET title='{new_title}' WHERE id='{map_id}'")
    db.commit()
    cursor.close()


if __name__ == '__main__':
    mode = input()
    assert mode in ('GET', 'DELETE', 'UPDATE')

    if mode == 'GET':
        print(get_index())
    elif mode == 'DELETE':
        map_id = input()
        delete_index(map_id)
    elif mode == 'UPDATE':
        map_id = input()
        new_title = input()
        update_index(map_id, new_title)
