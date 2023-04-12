import asyncio
import localSearch
from requests import get
from aiohttp.client import ClientSession, TCPConnector


with open('secrets.json', 'r') as secrets:
    localSearch.API_KEY = secrets.read().json()['bing_maps_api_key']
print(localSearch.API_KEY)

# documentation for request is here:
# https://nominatim.org/release-docs/develop/api/Search/#:~:text=Overpass%20API.-,Parameters,-%EF%83%81
request = "https://nominatim.openstreetmap.org/search.php?city=Monowi&state=Nebraska&polygon_geojson=1&format=json"
request_no_polygon = "https://nominatim.openstreetmap.org/search.php?city=Monowi&state=Nebraska&format=json"

"""bounding_box = get(request_no_polygon).json()[0]["boundingbox"]
bounding_box[2], bounding_box[1] = bounding_box[1], bounding_box[2]
bounding_box = tuple(map(float, bounding_box))"""

bounding_box = (42.826945, -98.3346076, 42.8315692, -98.324824)
requested_types = ["Restaurants"]
file_name = 'map1.json'

# newFile = open(file_name, "w")


async def download_link(url, session):
    async with session.get(url) as response:
        result = await response.json()
        newFile.write(result)


async def download_all(urls):
    # 5 is the max for Bing API
    my_conn = TCPConnector(limit=4)
    async with ClientSession(connector=my_conn) as session:
        tasks = []
        for grid in localSearch.search_grid(bounding_box, 2, 2):
            url = localSearch.construct_request(
                types=requested_types,
                maxResults=25,
                userMapView=grid
                )
            task = asyncio.ensure_future(
                download_link(url, session))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)
