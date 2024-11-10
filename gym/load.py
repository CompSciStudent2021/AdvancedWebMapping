import json
from pathlib import Path
from django.contrib.gis.geos import Point
from .models import GymLocation

# Path to the GeoJSON file
geojson_path = Path(__file__).resolve().parent / 'data' / 'gym_2d.geojson'

def run(verbose=True):
    # Load the GeoJSON data
    with geojson_path.open() as f:
        data = json.load(f)

    # Iterate over each feature in the GeoJSON
    for feature in data['features']:
        properties = feature.get('properties', {})
        geometry = feature.get('geometry', {})
        coordinates = geometry.get('coordinates', [])

        # Ensure coordinates are valid and discard the Z-coordinate
        if len(coordinates) < 2:
            if verbose:
                print("Skipping feature with missing coordinates")
            continue

        # Use only the X and Y coordinates to create a 2D point
        point = Point(coordinates[0], coordinates[1])  # Discard any Z value

        # Create or update each GymLocation entry
        obj, created = GymLocation.objects.update_or_create(
            objectid=properties.get('OBJECTID'),
            defaults={
                'location': properties.get('Location', ''),
                'type': properties.get('Type', ''),
                'itm_x': properties.get('ITM_X', None),
                'itm_y': properties.get('ITM_Y', None),
                'point': point,
            }
        )

        # Print status if verbose mode is enabled
        if verbose:
            action = "Created" if created else "Updated"
            print(f"{action} GymLocation: {obj}")

    print("Data loading complete.")
