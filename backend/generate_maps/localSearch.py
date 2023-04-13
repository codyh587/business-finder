"""
This module contains methods to assist with making requests for the Bing Maps
Local Search API.

Functions:
    validate_types: validates API business type IDs
    construct_request: constructs API request url
    validate_request_parameters: validates construct_request parameters
    parse_locations: generator that parses JSON data from an API response
    search_grid: generator that splits a search region into an even grid
"""
from numpy import arange


type_identifiers = {
    'EatDrink': {
        'Bars', 'BarsGrillsAndPubs', 'BelgianRestaurants',
        'BreweriesAndBrewPubs', 'BritishRestaurants', 'BuffetRestaurants',
        'CafeRestaurants', 'CaribbeanRestaurants', 'ChineseRestaurants',
        'CocktailLounges', 'CoffeeAndTea', 'Delicatessens', 'DeliveryService',
        'Diners', 'DiscountStores', 'Donuts', 'FastFood', 'FrenchRestaurants',
        'FrozenYogurt', 'GermanRestaurants', 'GreekRestaurants', 'Grocers',
        'Grocery', 'HawaiianRestaurants', 'HungarianRestaurants',
        'IceCreamAndFrozenDesserts', 'IndianRestaurants', 'ItalianRestaurants',
        'JapaneseRestaurants', 'Juices', 'KoreanRestaurants', 'LiquorStores',
        'MexicanRestaurants', 'MiddleEasternRestaurants', 'Pizza',
        'PolishRestaurants', 'PortugueseRestaurants', 'Pretzels',
        'Restaurants', 'RussianAndUkrainianRestaurants', 'Sandwiches',
        'SeafoodRestaurants', 'SpanishRestaurants', 'SportsBars',
        'SteakHouseRestaurants', 'Supermarkets', 'SushiRestaurants',
        'TakeAway', 'Taverns', 'ThaiRestaurants', 'TurkishRestaurants',
        'VegetarianAndVeganRestaurants', 'VietnameseRestaurants'
    },
    'SeeDo': {
        'AmusementParks', 'Attractions', 'Carnivals', 'Casinos',
        'LandmarksAndHistoricalSites', 'MiniatureGolfCourses', 'MovieTheaters',
        'Museums', 'Parks', 'SightseeingTours', 'TouristInformation', 'Zoos'
    },
    'Shop': {
        'AntiqueStores', 'Bookstores', 'CDAndRecordStores',
        'ChildrensClothingStores', 'CigarAndTobaccoShops', 'ComicBookStores',
        'DepartmentStores', 'DiscountStores', 'FleaMarketsAndBazaars',
        'FurnitureStores', 'HomeImprovementStores', 'JewelryAndWatchesStores',
        'KitchenwareStores', 'LiquorStores', 'MallsAndShoppingCenters',
        'MensClothingStores', 'MusicStores', 'OutletStores', 'PetShops',
        'PetSupplyStores', 'SchoolAndOfficeSupplyStores', 'ShoeStores',
        'SportingGoodsStores', 'ToyAndGameStores',
        'VitaminAndSupplementStores', 'WomensClothingStores'
    },
    'BanksAndCreditUnions': set(),
    'Hospitals': set(),
    'HotelsAndMotels': set(),
    'Parking': set()
}


def validate_types(types):
    """
    Verifies that a list of type IDs contains valid strings for the Local
    Search API type parameter.

    Args:
        types: a list, tuple, or set of strings containing type IDs. Space
        separated string also supported.

    Returns:
        True if every element in types is present in type_identifiers and False
        if not.
    """
    for type_id in types:
        found = False
        for category in type_identifiers:
            if type_id == category or type_id in type_identifiers[category]:
                found = True
                break

        if not found:
            return False
    return True


def construct_request(query=None,
                      types=None,
                      maxResults=None,
                      userCircularMapView=None,
                      userLocation=None,
                      userMapView=None,
                      key=None,
                      validate=False):
    """
    Constructs the URL for a Local Search API request given API parameters.

    Args:
        query: string representing a search query. Either query or types must
            be provided.
        types: a list, tuple, or set of strings containing type IDs. Either
            query or types must be provided. Space separated string also
            supported.
        maxResults: integer indicating the maximum amount of  results to
            retrieve (between 1-25).
        userCircularMapView: a list or tuple of 3 floats specifying the
            center location (latitude, longitude) and radius (m) of a circular
            region to search from. Cannot be used with userMapView.
        userLocation: a list or tuple of 2-3 floats specifying the target
            location (latitude, longitude) and radius (m, optional)
            representing the confidence in the accuracy of the location. Does
            nothing if userCircularMapView or userMapView are provided.
        userMapView: a list or tuple of 4 floats specifying two corners of a
            rectangular search region, in order of:
                - Latitude of the Southwest corner
                - Longitude of the Southwest corner
                - Latitude of the Northeast corner
                - Longitude of the Northeast corner
            Cannot be used with userCircularMapView.
        key: string representing the API key. Must be provided.
        validate: boolean toggling optional parameter validation.

    Returns:
        A string representing the URL for the desired API request.

    Raises:
        Applies when validate is set to True.

        ValueError: if type IDs are invalid.
        ValueError: if maxResults is not between 1-25.
        ValueError: if neither query nor type are provided.
        ValueError: if both userCircularMapView and userMapView are provided.
        ValueError: if userMapView coordinates do not form a rectangle.
        ValueError: if key is not provided.
    """
    if type(types) is str:
        types = types.split()
    if validate:
        validate_request_parameters(query, types, maxResults,
                                    userCircularMapView, userLocation,
                                    userMapView, key)

    url = f"https://dev.virtualearth.net/REST/v1/LocalSearch/?key={key}"
    if query:
        url += f"&query={query.replace(' ', '%20')}"
    if types:
        url += f"&type={','.join(types)}"
    if maxResults:
        url += f"&maxResults={int(maxResults)}"
    if userCircularMapView:
        url += (
            f"&userCircularMapView={','.join(map(str, userCircularMapView))}")
    if userLocation:
        url += f"&userLocation={','.join(map(str, userLocation))}"
    if userMapView:
        url += f"&userMapView={','.join(map(str, userMapView))}"

    return url


def validate_request_parameters(query, types, maxResults, userCircularMapView,
                                userLocation, userMapView, key=None):
    """
    Helper method to perform optional construct_request() parameter validation.
    Does not validate specfied data types.
    """
    if not query and not types:
        raise ValueError("Either query or types must be provided")
    if types and not validate_types(types):
        raise ValueError("types contains invalid type IDs")
    if maxResults and not (1 <= maxResults <= 25):
        raise ValueError("maxResults must be between 1-25")
    if userCircularMapView and userMapView:
        raise ValueError("userCircularMapView and userMapView cannot both be" +
                         "provided")
    if userMapView:
        sw_lat, sw_long, ne_lat, ne_long = userMapView
        if sw_lat > ne_lat or sw_long > ne_long:
            raise ValueError("userCircularMapView coordinates must form a" +
                             "rectangle (sw_lat < ne_lat, sw_long < ne_long)")
    if not key:
        raise ValueError("key must be provided")


def parse_locations(response, items=None):
    """
    Generator that retrieves location data from a JSON response given by the
    Local Search API. Can retrieve specifed attributes from each search result.

    Args:
        response: dictionary created from a Local Search API JSON response.
            Dictionary must contain entire JSON document.
        items: a list or tuple containing strings specifying the desired yield
            attributes.

            Attribute Hierarchy:
                > '__type'
                > 'name'
                v 'point'
                    > 'type'
                    v 'coordinates'
                        > list (size 2)
                v 'Address'
                    > 'addressLine'
                    > 'adminDistrict'
                    > 'countryRegion'
                    > 'formattedAddress'
                    > 'locality'
                    > 'postalCode'
                > 'PhoneNumber'
                > 'Website'
                > 'entityType'
                v 'geocodePoints'
                    v list (size 1)
                        > 'type'
                        v 'coordinates'
                            > list (size 2)
                        > 'calculationMethod'
                        v 'usageTypes'
                            > list (size 1)

            To retrieve a specific attribute from a location, indicate the
            hierarchy separated by dots. To retrieve an element from a list,
            type the index number.

            Ex: to retrieve name and calculationMethod, set
            items=["name", "geocodePoints.0.calculationMethod"].

    Yields:
        A list of string values corresponding to attributes specified in items
        for each search result, in identical order. Returns None if attribute
        does not exist. Returns dictionary of
        entire search result if items is not specified.

    Raises:
        KeyError: if JSON dictionary is invalid.
    """
    if items:
        items_split = tuple(tuple(item.split(".")) for item in items)
    for location_dict in response['resourceSets'][0]['resources']:
        if not items:
            yield location_dict
        else:
            location_data = []
            for item_levels in items_split:
                try:
                    data_entry = location_dict[item_levels[0]]
                    for item_level in item_levels[1:]:
                        if item_level.isdigit():
                            item_level = int(item_level)
                        data_entry = data_entry[item_level]
                except KeyError:
                    data_entry = None
                location_data.append(data_entry)

            yield location_data


def search_grid(coordinates, lat_partition, long_partition, set_size=False):
    """
    Generator that splits a rectangular search region into evenly distributed
    search grids.

    Args:
        coordinates: a list or tuple of 4 floats specifying two corners of a
            rectangular search region, in order of:
                - Latitude of the Southwest corner
                - Longitude of the Southwest corner
                - Latitude of the Northeast corner
                - Longitude of the Northeast corner
        lat_partition: integer or float representing the divisor used to
            separate the search region by latitude. Must be positive.

            Ex: Set lat_partition=2 to split the search region into halves
            latitudinally.
        long_partition: integer or float representing the divisor used to
            separate the search region by longitude. Must be positive.

            Ex: Set long_partition=2 to split the search region into halves
            longitudinally.
        set_size: boolean toggling set_size mode. set_size mode will use
            lat_partition and long_partition as the size of each grid instead
            of its divisor.

            Ex: Set lat_partition=2, long_partition=2, and set_size=True to
            split a rectangular search region into 2x2 degree grids rather than
            into quarters.

    Yields:
        A tuple of 4 floats specifying the southwest corner (latitude,
        longitude) and northeast corner (latitude, longitude) of each separate
        grid in the search region.

    Raises:
        ValueError: if coordinates do not form a rectangle.
        ValueError: if lat_partition or long_partition are not positive.
    """
    sw_lat, sw_long, ne_lat, ne_long = coordinates

    if sw_lat > ne_lat or sw_long > ne_long:
        raise ValueError("Coordinates must form a rectangle (sw_lat < " +
                         "ne_lat, sw_long < ne_long)")
    if lat_partition <= 0 or long_partition <= 0:
        raise ValueError("lat_partition and long_partition must be positive")

    if not set_size:
        lat_step = (ne_lat - sw_lat) / lat_partition
        long_step = (ne_long - sw_long) / long_partition
    else:
        lat_step = lat_partition
        long_step = long_partition

    for grid_lat in arange(sw_lat, ne_lat, lat_step):
        for grid_long in arange(sw_long, ne_long, long_step):
            yield (grid_lat, grid_long, min(grid_lat + lat_step, ne_lat),
                   min(grid_long + long_step, ne_long))
