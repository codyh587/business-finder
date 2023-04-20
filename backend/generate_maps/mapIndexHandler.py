"""
This module contains methods to assist with handling the map index JSON file,
named map_index.json.

map_index.json contains an array of JSON objects with the following attributes:
    "id": string representing a base-64 unique identifier for a given map.
    "title": string representing the user-created name for a given map.
    "location": a list of 2 floats specifying the coordinate location for the
        specfied city

Each object in map_index corresponds to a file in the /maps directory. The file
name for any corresponding map is id.json.

Global Variables:
    MAP_ID_LENGTH: length of the base-64 string for map_index attribute "id"
    MAP_ID_RETRY_LIMIT: retry limit for creating map_index attribute "id"

Functions:
    create_index: creates a unique base-64 map id and entry in map_index.json
    delete_index: deletes an entry from map_index and its corresponding file
    update_index: updates an entry from map_index for attribute "title"

When invoked directly, the following input values can be used to call
delete_index and update_index:

Input Values:
    mode: string specifying "DELETE" or "UPDATE"
    index_path: string representing the file path of map_index.json
    map_id: string representing the base-64 unique identifier for the given map
    new_title: string specifying the new value for attribute "title"
"""
from json import dump, loads
from os import remove
from os.path import exists, getsize
from secrets import token_urlsafe


MAP_ID_LENGTH = 10 * 3//4   # multiply length by 3/4 due to Base64 encoding
MAP_ID_RETRY_LIMIT = 10000


def ensure_exists(index_path):
    if not exists(index_path) or getsize(index_path) == 0:
        with open(index_path, 'w') as index_file:
            dump([], index_file)


def create_index(index_path, map_title, location, bounds):
    ensure_exists(index_path)
    with open(index_path, 'r') as index_file:
        index = loads(index_file.read())
        covered_names = set(entry['id'] for entry in index)

    new_id = token_urlsafe(MAP_ID_LENGTH)
    iterations = 0
    while new_id in covered_names:
        new_id = token_urlsafe(MAP_ID_LENGTH)
        iterations += 1
        if iterations >= MAP_ID_RETRY_LIMIT:
            raise ValueError("Map ID creation failed")

    index.append({
        'id': new_id,
        'title': map_title,
        'location': location,
        'bounds': bounds
    })

    with open(index_path, 'w') as index_file:
        dump(index, index_file)

    return new_id


def delete_index(index_path, map_id):
    ensure_exists(index_path)
    with open(index_path, 'r') as index_file:
        index = loads(index_file.read())

    index = [entry for entry in index if entry['id'] != map_id]

    try:
        remove(index_path[:index_path.rfind('\\') + 1] + map_id + '.json')
    except OSError:
        pass

    with open(index_path, 'w') as index_file:
        dump(index, index_file)


def update_index(index_path, map_id, new_title):
    ensure_exists(index_path)
    with open(index_path, 'r') as index_file:
        index = loads(index_file.read())

    new_index = []
    for entry in index:
        if entry['id'] == map_id:
            new_entry = entry
            new_entry['title'] = new_title
            new_index.append(new_entry)
        else:
            new_index.append(entry)

    with open(index_path, 'w') as index_file:
        dump(index, index_file)


if __name__ == '__main__':
    mode = input()
    assert mode == 'DELETE' or mode == 'UPDATE'
    index_path = input()
    map_id = input()

    if mode == 'DELETE':
        delete_index(index_path, map_id)
    elif mode == 'UPDATE':
        new_title = input()
        update_index(index_path, map_id, new_title)
