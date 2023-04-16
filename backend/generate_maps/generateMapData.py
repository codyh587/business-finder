from asyncio import ensure_future, gather, run
from aiohttp.client import ClientSession, TCPConnector
from json import dump, loads
from localSearch import construct_request, parse_locations, search_grid
from mapIndexHandler import create_index
from os.path import dirname
from requests import get


# Retrieve input values
city = 'Monowi'
state = 'Nebraska'
title = 'Monowi Map'
requested_types = ['Restaurants']

# Retrieve Bing Maps API key
file_path = dirname(__file__)
with open(f'{file_path}\secrets.json', 'r') as secrets:
    bing_maps_api_key = loads(secrets.read())['bing_maps_api_key']


# Retrieve city bounding box
nominatim_request = get(
    "https://nominatim.openstreetmap.org/search.php?format=json&city=" + city
    + "&state=" + state
)
bounding_box = nominatim_request.json()[0]['boundingbox']
bounding_box[2], bounding_box[1] = bounding_box[1], bounding_box[2]
# (30, -120, 50, -90)
bounding_box = tuple(map(float, bounding_box))


# Create asynchronous Bing Maps API request functions
desired_attributes = ('name', 'point.coordinates', 'Address.formattedAddress',
                      'entityType')


async def retrieve(url, session):
    async with session.get(url) as response:
        results = await response.json()
        for name, coordinates, address, business_type in parse_locations(
            results, desired_attributes
        ):
            # TODO: Check and validate coordinate is inside the city
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
        for grid in search_grid(bounding_box, 2, 2):
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


# TODO Create unique map filename
map_index_path = f'{file_path}\maps\map_index.json'
map_file_name = '1.json'
map_file_name = create_index(map_index_path, title)


# Create map data
map_objects = []
covered_addresses = set()
with open(
    f'{file_path}\maps\{map_file_name}', 'w', encoding='utf-8'
) as map_file:
    run(retrieve_all())
    dump(
        {'data': map_objects},
        map_file,
        ensure_ascii=False
    )
