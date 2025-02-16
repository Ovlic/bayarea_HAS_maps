"""import requests
import json
import folium
import math
from utils import makeBeautifyIcon
from my_session import MySession

# 511 API key
key = "api_key"
session = MySession(key)

# Ignored lines (duplicate stations)
ignored_lines = []

# Train operators
operators = ['CE', 'BA', 'CT', 'AM', 'SI', 'SF', 'SA', 'SC']

# Define the map
m = folium.Map(
    location=[37.65077186632317, -122.24094250022335],
    zoom_start=9,
)

# Load stations from file
with open('stations.json', 'r') as f:
    stations = json.loads(f.read())

# Define bounds for the map (approximate bounding box of the area)
map_bounds = [
    [-123.0, 37.0],  # Southwest corner (lon, lat)
    [-121.0, 38.0],  # Northeast corner (lon, lat)
]

# Generate a large polygon for the map bounds
outer_polygon = [
    [map_bounds[0][1], map_bounds[0][0]],  # SW corner
    [map_bounds[1][1], map_bounds[0][0]],  # NW corner
    [map_bounds[1][1], map_bounds[1][0]],  # NE corner
    [map_bounds[0][1], map_bounds[1][0]],  # SE corner
    [map_bounds[0][1], map_bounds[0][0]],  # Back to SW corner
]

# Collect all the circle centers and radii
holes = []
for op in operators:
    for line_id in stations[op]:
        for stop in stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
            # to number
            lat = float(stop["Location"]["Latitude"])
            lon = float(stop["Location"]["Longitude"])
            # lat = stop["Location"]["Latitude"]
            # lon = stop["Location"]["Longitude"]
            

            # Add marker
            folium.Marker(
                location=[lat, lon],
                popup=stop['Name'],
                icon=makeBeautifyIcon(
                    icon=None,
                    border_color="#000000",
                    border_width=3,
                    text_color="#b3334f",
                    icon_shape="circle",
                    inner_icon_style="opacity: 0;",
                    icon_size=[13, 13],
                )
            ).add_to(m)

            # Add circle hole (approximation as a polygon)
            circle_coords = []
            for i in range(72):  # Approximate circle with 72 points
                angle = i * (360 / 72)
                d_lat = 402.336 / 6378137 * math.cos(math.radians(angle))  # Radius in meters
                d_lon = 402.336 / 6378137 * math.sin(math.radians(angle)) / math.cos(math.radians(lat))
                circle_coords.append([lat + math.degrees(d_lat), lon + math.degrees(d_lon)])
            holes.append(circle_coords)

# Create GeoJSON with the large polygon and holes
polygon_with_holes = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [outer_polygon] + holes,  # Main polygon and holes
            },
            "properties": {
                "fill": "#000000",  # Black shading for outside
                "fill-opacity": 0.6,
                "stroke": False,
            },
        }
    ],
}

# Add the shaded area to the map
folium.GeoJson(
    polygon_with_holes,
    style_function=lambda x: {
        'fillColor': x['properties']['fill'],
        'fillOpacity': x['properties']['fill-opacity'],
        'color': 'none'
    }
).add_to(m)

# Save the map
m.save('circle_shade.html')
"""

import requests
import json
import folium
import math
from utils import makeBeautifyIcon
from my_session import MySession

# 511 API key
key = "api_key"
session = MySession(key)

# Ignored lines (duplicate stations)
ignored_lines = []

# Train operators
operators = ['CE', 'BA', 'CT', 'AM', 'SI', 'SF', 'SA', 'SC']

# Define the map
m = folium.Map(
    location=[37.65077186632317, -122.24094250022335],
    zoom_start=9,
)

# Load stations from file
with open('stations.json', 'r') as f:
    stations = json.loads(f.read())

# Define bounds for the map (approximate bounding box of the area)
map_bounds = [
    [-123.0, 37.0],  # Southwest corner (lon, lat)
    [-121.0, 38.0],  # Northeast corner (lon, lat)
]

# Generate a large polygon for the map bounds
outer_polygon = [
    [map_bounds[0][0], map_bounds[0][1]],  # SW corner (lon, lat)
    [map_bounds[0][0], map_bounds[1][1]],  # NW corner
    [map_bounds[1][0], map_bounds[1][1]],  # NE corner
    [map_bounds[1][0], map_bounds[0][1]],  # SE corner
    [map_bounds[0][0], map_bounds[0][1]],  # Back to SW corner
]

# Collect all the circle centers and radii
holes = []
for op in operators:
    for line_id in stations[op]:
        for stop in stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
            lat = float(stop["Location"]["Latitude"])
            lon = float(stop["Location"]["Longitude"])

            # Add marker
            folium.Marker(
                location=[lat, lon],
                popup=stop['Name'],
                icon=makeBeautifyIcon(
                    icon=None,
                    border_color="#000000",
                    border_width=3,
                    text_color="#b3334f",
                    icon_shape="circle",
                    inner_icon_style="opacity: 0;",
                    icon_size=[13, 13],
                )
            ).add_to(m)

            # Add circle hole (approximation as a polygon)
            circle_coords = []
            for i in range(72):  # Approximate circle with 72 points
                angle = math.radians(i * (360 / 72))
                d_lat = (402.336 / 6378137) * math.cos(angle)  # Convert radius to degrees
                d_lon = (402.336 / 6378137) * math.sin(angle) / math.cos(math.radians(lat))
                circle_coords.append([lon + math.degrees(d_lon), lat + math.degrees(d_lat)])
            circle_coords.append(circle_coords[0])  # Close the ring
            holes.append(circle_coords)

# Create GeoJSON with the large polygon and holes
polygon_with_holes = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [outer_polygon] + holes,  # Main polygon and holes
            },
            "properties": {
                "fill": "#000000",  # Black shading for outside
                "fill-opacity": 0.6,
                "stroke": False,
            },
        }
    ],
}

# Add the shaded area to the map
folium.GeoJson(
    polygon_with_holes,
    style_function=lambda x: {
        'fillColor': '#000000',
        'fillOpacity': 0.6,
        'color': 'none',
    }
).add_to(m)

# Save the map
m.save('circle_shade.html')
print("Map with shaded area saved as circle_shade.html")
