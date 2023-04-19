"""
This module contains methods to assist with verifying input values in
generateMapData.py

Functions:
    verify_map_values: verifies a variety of input values for
        generating map data in generateMapData.py
"""
from localSearch import validate_request_parameters


def verify_map_inputs(city, state, title, types, maxResults, key, tcp_limit,
                      nominatim_response):
    validate_request_parameters(types=types, maxResults=maxResults, key=key)

    if not tcp_limit or not (1 <= tcp_limit <= 5):
        raise ValueError("tcp_limit must be between 1-5")
    if not city or not state or not title:
        raise ValueError("city, state, and title must be provided")
    if not nominatim_response:
        raise ValueError("nominatim request failed, check city and state")
