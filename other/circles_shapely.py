"""import requests
import json
import folium
import math
from shapely.geometry import Polygon, Point, mapping
from shapely.ops import unary_union
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
    [-123.0, 36.5],  # Southwest corner (lon, lat)
    [-121.0, 39.0],  # Northeast corner (lon, lat)
]

# Create the outer polygon using Shapely
outer_polygon = Polygon([
    (map_bounds[0][0], map_bounds[0][1]),  # SW corner
    (map_bounds[1][0], map_bounds[0][1]),  # NW corner
    (map_bounds[1][0], map_bounds[1][1]),  # NE corner
    (map_bounds[0][0], map_bounds[1][1]),  # SE corner
    (map_bounds[0][0], map_bounds[0][1]),  # Back to SW corner
])

# Collect all the circle polygons
circle_shapes = []
for op in operators:
    for line_id in stations[op]:
        for stop in stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
            # Extract coordinates
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

            # Create a circle using Shapely
            circle = Point(lon, lat).buffer(402.336 / 6378137 * 360 / (2 * math.pi))  # Approximate circle
            circle_shapes.append(circle)

# Compute the union of all circles
merged_circles = unary_union(circle_shapes)

# Subtract the merged circles from the outer polygon
shaded_area = outer_polygon.difference(merged_circles)

# Convert the shaded area into a GeoJSON format
shaded_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": mapping(shaded_area),  # Convert Shapely geometry to GeoJSON format
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
    shaded_geojson,
    style_function=lambda x: {
        'fillColor': x['properties']['fill'],
        'fillOpacity': x['properties']['fill-opacity'],
        'color': 'none'
    }
).add_to(m)


# Add measurement tool
m.add_child(folium.plugins.MeasureControl())
# Save the map
m.save('circle_shade.html')
"""
import requests
import json
import folium
import math
from shapely.geometry import Polygon, Point, mapping
from shapely.ops import unary_union
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

# Define bounds for the map (adjust northern boundary to raise the rectangle)
map_bounds = [
    [-123.0, 36.5],  # Southwest corner (lon, lat)
    [-121.0, 39.0],  # Northeast corner (lon, lat)
]

# Create the outer polygon using Shapely
outer_polygon = Polygon([
    (map_bounds[0][0], map_bounds[0][1]),  # SW corner
    (map_bounds[1][0], map_bounds[0][1]),  # NW corner
    (map_bounds[1][0], map_bounds[1][1]),  # NE corner
    (map_bounds[0][0], map_bounds[1][1]),  # SE corner
    (map_bounds[0][0], map_bounds[0][1]),  # Back to SW corner
])

# Collect all the circle polygons
circle_shapes = []
for op in operators:
    for line_id in stations[op]:
        for stop in stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
            # Extract coordinates
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

            # Create a circle with accurate scaling
            """radius_meters = 402.336  # Circle radius in meters
            earth_radius = 6378137  # Earth's radius in meters

            # Convert radius to degrees
            lat_radius = radius_meters / earth_radius * (180 / math.pi)
            lon_radius = radius_meters / (earth_radius * math.cos(math.radians(lat))) * (180 / math.pi)

            # Create a circle as a Shapely Polygon
            circle = Point(lon, lat).buffer(lon_radius, resolution=72)
            circle_shapes.append(circle)"""
            """# Create a circle with accurate scaling
            radius_meters = 402.336  # Circle radius in meters
            earth_radius = 6378137  # Earth's radius in meters

            # Convert radius to degrees
            lat_radius = radius_meters / earth_radius * (180 / math.pi)
            lon_radius = radius_meters / (earth_radius * math.cos(math.radians(lat))) * (180 / math.pi)

            # Create a circle as a Shapely Polygon
            circle = Point(lon, lat).buffer(lon_radius, resolution=72)
            circle_shapes.append(circle)"""
            """# Create a circle with accurate scaling
            radius_meters = 402.336  # Circle radius in meters
            earth_radius = 6378137  # Earth's radius in meters

            # Convert radius to degrees 
            radius_degrees = radius_meters / earth_radius * (180 / math.pi) 

            # Create a circle as a Shapely Polygon (using radius in degrees)
            circle = Point(lon, lat).buffer(radius_degrees, resolution=72)  
            circle_shapes.append(circle) # Working vertical axis, horizontal = .20 miles"""
            # Create a circle with accurate scaling
            radius_meters = 402.336  # Circle radius in meters
            earth_radius = 6378137  # Earth's radius in meters

            # Convert radius to degrees
            lat_radius = radius_meters / earth_radius * (180 / math.pi)

            # Adjust the radius for longitude based on the latitude (cosine of the latitude)
            lon_radius = radius_meters / (earth_radius * math.cos(math.radians(lat))) * (180 / math.pi)

            # Create a circle as a Shapely Polygon using latitude and longitude radius
            circle = Point(lon, lat).buffer(lon_radius, resolution=72)  # Using lon_radius for the buffer
            circle_shapes.append(circle)



            

# Compute the union of all circles
merged_circles = unary_union(circle_shapes)

# Subtract the merged circles from the outer polygon
shaded_area = outer_polygon.difference(merged_circles)

# Convert the shaded area into a GeoJSON format
shaded_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": mapping(shaded_area),  # Convert Shapely geometry to GeoJSON format
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
    shaded_geojson,
    style_function=lambda x: {
        'fillColor': x['properties']['fill'],
        'fillOpacity': x['properties']['fill-opacity'],
        'color': 'none'
    }
).add_to(m)

# Add measurement tool
m.add_child(folium.plugins.MeasureControl())
# Save the map
m.save('circle_shade.html')
