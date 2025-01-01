import requests
from django.core.cache import cache

def fetch_osm_gyms(bbox):
    """
    Fetch gym locations from OpenStreetMap using the Overpass API with caching.
    :param bbox: Tuple of (south, west, north, east) bounding box coordinates.
    :return: List of gyms with name, latitude, and longitude.
    """
    cache_key = f"osm_gyms_{bbox}"
    cached_gyms = cache.get(cache_key)
    if cached_gyms:
        return cached_gyms

    url = "https://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:25];
    node["leisure"="fitness_centre"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    out body;
    """

    try:
        response = requests.post(url, data={"data": query})
        response.raise_for_status()

        if "application/json" not in response.headers.get("Content-Type", ""):
            print("Non-JSON response received:", response.text)
            return []  # Return an empty list for invalid responses

        data = response.json()
        gyms = []
        for element in data.get("elements", []):
            gyms.append({
                "name": element.get("tags", {}).get("name", "Unnamed"),
                "latitude": element["lat"],
                "longitude": element["lon"],
            })

        cache.set(cache_key, gyms, timeout=3600)
        return gyms
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Overpass API: {e}")
        return []


def fetch_osm_locations(location_type, bbox, sport_type=None):
    """
    Fetch locations from OpenStreetMap using the Overpass API with caching.
    :param location_type: The type of location to fetch (e.g., 'football_pitch').
    :param bbox: Tuple of (south, west, north, east) bounding box coordinates.
    :param sport_type: The type of sport to filter by (e.g., 'football', 'gaelic_games').
    :return: List of locations with name, latitude, and longitude.
    """
    cache_key = f"osm_locations_{location_type}_{sport_type}_{bbox}"
    cached_locations = cache.get(cache_key)
    if cached_locations:
        return cached_locations

    url = "https://overpass-api.de/api/interpreter"
    
    # Add sport type filter if provided
    sport_filter = f'["sport"="{sport_type}"]' if sport_type else ""
    
    query = f"""
    [out:json][timeout:25];
    node{sport_filter}["leisure"="{location_type}"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    out body;
    """

    try:
        response = requests.post(url, data={"data": query})
        response.raise_for_status()  # Raise an error for HTTP issues

        if "application/json" not in response.headers.get("Content-Type", ""):
            print("Non-JSON response received:", response.text)
            return []  # Return an empty list to avoid breaking the app

        data = response.json()

        locations = []
        for element in data.get("elements", []):
            locations.append({
                "name": element.get("tags", {}).get("name", "Unnamed"),
                "latitude": element["lat"],
                "longitude": element["lon"],
            })

        cache.set(cache_key, locations, timeout=3600)
        return locations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Overpass API: {e}")
        return []
