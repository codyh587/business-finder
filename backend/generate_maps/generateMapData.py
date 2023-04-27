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
    "p": string representing the phone number for the retrieved business
    "w": string representing the website for the retrieved business

Global Variables:
    LAT_PART: float for lat_size parameter in localSearch.search_grid()
    LONG_PART: float for long_partition parameter in localSearch.search_grid()
    SET_SIZE: boolean for set_size parameter in localSearch.search_grid()
    TCP_LIMIT: int for maximum concurrent TCP connections for Bing Maps API
        requests (limit is 5)
    MAX_RESULTS: int for maximum payload size for Bing Maps API responses
        (limit is 25)
    BING_MAPS_KEY: string for Bing Maps API key located in
        generate_maps/secrets.json with key "BING_MAPS_KEY"

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
from verifyMapInputs import verify_map_inputs


# Global Variables
LAT_PART = 5
LONG_PART = 8
SET_SIZE = False
TCP_LIMIT = 4
MAX_RESULTS = 25
FILE_PATH = dirname(__file__)

# Retrieve Bing Maps API key
with open(f'{FILE_PATH}\secrets.json', 'r') as secrets:
    BING_MAPS_KEY = loads(secrets.read())['BING_MAPS_KEY']
print("Retrieved API key")

# Retrieve input values
city = input()
state = input()
title = input()
requested_types = tuple(input().split(','))
print("Retrieved input values")

# Send Nominatim API request
nominatim_request_url = ("https://nominatim.openstreetmap.org/search.php?" +
    "format=json&city=" + city + "&state=" + state)
nominatim_response = get(nominatim_request_url).json()
print("Received Nominatim response")

# Verify map input values
verify_map_inputs(city,
                  state,
                  title,
                  requested_types,
                  MAX_RESULTS,
                  BING_MAPS_KEY,
                  TCP_LIMIT,
                  nominatim_response)

# Retrieve city location and bounding box
location = [
    float(nominatim_response[0]['lat']),
    float(nominatim_response[0]['lon'])
]
bounding_box = nominatim_response[0]['boundingbox']
bounding_box[2], bounding_box[1] = bounding_box[1], bounding_box[2]
bounding_box = tuple(map(float, bounding_box))
print("Retrieved location", location)
print("Retrieved bounding box", bounding_box)

# Create asynchronous Bing Maps API request functions
desired_attributes = ('name', 'point.coordinates', 'Address.formattedAddress',
                      'entityType', 'PhoneNumber', 'Website')


async def retrieve(url, session):
    async with session.get(url) as response:
        results = await response.json()
        for name, coords, add, bus_type, phone, website in parse_locations(
            results, desired_attributes
        ):
            map_object = {
                'n': name,
                'c': coords,
                'a': add,
                't': bus_type,
                'p': phone,
                'w': website
            }
            if add not in covered_addresses:
                map_objects.append(map_object)
                covered_addresses.add(add)


async def retrieve_all():
    connector = TCPConnector(limit=TCP_LIMIT)
    async with ClientSession(connector=connector) as session:
        tasks = []
        for grid in search_grid(bounding_box, LAT_PART, LONG_PART, SET_SIZE):
            for requested_type in requested_types:
                url = construct_request(
                    types=requested_type,
                    maxResults=MAX_RESULTS,
                    userMapView=grid,
                    key=BING_MAPS_KEY
                )
                task = ensure_future(retrieve(url, session))
                tasks.append(task)

        await gather(*tasks, return_exceptions=True)


# Create map id and entry in map index
map_file_name = create_index(
    title,
    location,
    list(bounding_box)
)
print("Created map index entry")

# Generate and write map data
map_objects = []
covered_addresses = set()
with open(
    f'{FILE_PATH}\maps\{map_file_name}.json', 'w', encoding='utf-8'
) as map_file:
    print("Created map file")
    run(retrieve_all())
    print("Completed async requests")
    dump(
        map_objects,
        map_file,
        ensure_ascii=False
    )

print("Finished map generation")
