"""
This module contains methods to assist with handling the map index JSON file,
named map_index.json.

map_index.json contains an array of JSON objects with the following attributes:
    "id": int
    "title": str

Each object in map_index corresponds to a file in the /maps directory. The file
name for any corresponding map will be id.json. "title" corresponds to the
user-created name for the generated map.

Global Variables:
    MAP_ID_LENGTH: length of the base-64 string for map_index attribute "id"
    MAP_ID_RETRY_LIMIT: retry limit for creating map_index attribute "id"

Functions:
    create_index: creates a random base-64 map id and entry in map_index.json
    delete_index: deletes an entry from map_index and its corresponding file
"""
from json import dump, loads
from os import remove
from os.path import exists, getsize
from secrets import token_urlsafe


MAP_ID_LENGTH = 10
MAP_ID_RETRY_LIMIT = 10000


def ensure_exists(index_path):
    if not exists(index_path) or getsize(index_path) == 0:
        with open(index_path, 'w') as index_file:
            dump([], index_file)


# creates a unique ID comparing it with ones in map_index.json
def create_index(index_path, map_title):
    ensure_exists(index_path)
    with open(index_path, 'r') as index_file:
        index = loads(index_file.read())
        covered_names = set(entry['id'] for entry in index)

    new_id = token_urlsafe(MAP_ID_LENGTH * 3//4)
    iterations = 0
    while new_id in covered_names:
        new_id = token_urlsafe(MAP_ID_LENGTH * 3//4)
        iterations += 1
        if iterations >= MAP_ID_RETRY_LIMIT:
            raise ValueError("Map ID creation failed")

    index.append({
        'id': new_id,
        'title': map_title
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
