from asyncio import ensure_future, gather, run
from aiohttp.client import ClientSession, TCPConnector
from localSearch import construct_request, parse_locations, search_grid
from json import loads
from os.path import dirname
from requests import get


# Retrieve input values
city = 'Monowi'
state = 'Nebraska'
requested_types = ['Restaurants']
file_path = dirname(__file__)
with open(file_path + '\secrets.json') as secrets:
    bing_maps_api_key = loads(secrets.read())['bing_maps_api_key']

# Retrieve city bounding box
nominatim_request = get(
    "https://nominatim.openstreetmap.org/search.php?format=json&city=" + city
    + "&state=" + state
)
bounding_box = nominatim_request.json()[0]['boundingbox']
bounding_box[2], bounding_box[1] = bounding_box[1], bounding_box[2]
# (42.826945, -98.3346076, 42.8315692, -98.324824) or (30, -120, 50, -90)
bounding_box = tuple(map(float, bounding_box))

# Prepare map creation TODO make this json
map_file_name = 'map1.txt'
map_file = open(file_path + '\maps\\' + map_file_name, 'w')
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
            } # TODO write in json
            map_file.write(str(map_object))


async def retrieve_all():
    # 5 is the max for Bing API
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


run(retrieve_all())
map_file.close()
