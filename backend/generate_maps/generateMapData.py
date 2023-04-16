"""
This module generates a JSON file containing location data for specified
business types in a designated city (referred to as a map).

Each map file is given a unique base-64 identifier and placed in the /maps
directory. An entry for each map is also created in map_index.json for
indexing purposes.

Each map file contains an array of JSON objects with the following attributes:
    "n": string representing the name for the retrieved business
    "c": a list of 2 floats specifying the coordinate location for the
        retrieved business
    "a": string representing the address for the retrieved business
    "t": string representing the business type for the retrieved business

Input Values:
    city: string representing the desired city to search
    state: string representing the state of the desired city to search
    title: string representing the user-created name for the generated map
    requested_types: a list or tuple of strings specifying the desired Bing
        Maps API business type identifiers

This module uses the Bing Maps API and Nominatim API.
"""
from asyncio import ensure_future, gather, run
from aiohttp.client import ClientSession, TCPConnector
from json import dump, loads
from localSearch import construct_request, parse_locations, search_grid
from mapIndexHandler import create_index
from os.path import dirname
from requests import get


# Retrieve input values
city = input()
state = input()
title = input()
requested_types = tuple(input().split(','))
print("Retrieved input values")

# Retrieve Bing Maps API key
file_path = dirname(__file__)
with open(f'{file_path}\secrets.json', 'r') as secrets:
    bing_maps_api_key = loads(secrets.read())['bing_maps_api_key']
print("Retrieved API key")

# Retrieve city bounding box
nominatim_request = get(
    "https://nominatim.openstreetmap.org/search.php?format=json&city=" + city
    + "&state=" + state
)
bounding_box = nominatim_request.json()[0]['boundingbox']
bounding_box[2], bounding_box[1] = bounding_box[1], bounding_box[2]
bounding_box = tuple(map(float, bounding_box))
print("Retrieved bounding box", bounding_box)

# Create asynchronous Bing Maps API request functions
desired_attributes = ('name', 'point.coordinates', 'Address.formattedAddress',
                      'entityType')


async def retrieve(url, session):
    async with session.get(url) as response:
        results = await response.json()
        for name, coordinates, address, business_type in parse_locations(
            results, desired_attributes
        ):
            # TODO: Validate coordinates is inside the city
            map_object = {
                'n': name,
                'c': coordinates,
                'a': address,
                't': business_type
            }
            if address not in covered_addresses:
                map_objects.append(map_object)
                covered_addresses.add(address)


async def retrieve_all():
    # 5 is the max for Bing Maps API
    connector = TCPConnector(limit=4)
    async with ClientSession(connector=connector) as session:
        tasks = []
        for grid in search_grid(bounding_box, 1, 1):
            for requested_type in requested_types:
                url = construct_request(
                    types=requested_type,
                    maxResults=25,
                    userMapView=grid,
                    key=bing_maps_api_key
                )
                task = ensure_future(retrieve(url, session))
                tasks.append(task)

        await gather(*tasks, return_exceptions=True)


# Create map id and entry in map index
map_index_path = f'{file_path}\maps\map_index.json'
map_file_name = create_index(map_index_path, title)
print("Map index entry created")

# Generate and write map data
map_objects = []
covered_addresses = set()
with open(
    f'{file_path}\maps\{map_file_name}.json', 'w', encoding='utf-8'
) as map_file:
    print("Map file created")
    run(retrieve_all())
    print("Async requests completed")
    dump(
        map_objects,
        map_file,
        ensure_ascii=False
    )
