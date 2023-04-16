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
"""
from json import dump, loads
from os.path import exists
from secrets import token_urlsafe


MAP_ID_LENGTH = 5
MAP_ID_RETRY_LIMIT = 10000


def ensure_exists(index_path):
    if not exists(index_path):
        with open(index_path, 'w') as index_file:
            dump([], index_file)


# creates a unique ID comparing it with ones in map_index.json
def create_index(index_path, map_title):
    ensure_exists(index_path)
    with open(index_path, 'r+') as index_file:
        index = loads(index_file.read())
        covered_names = set(entry['file'] for entry in index)

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
        dump(index, index_file)

    return new_id
