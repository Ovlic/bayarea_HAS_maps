import json
import math
from shapely.geometry import Polygon, mapping, Point
from shapely.ops import unary_union
import dash
from dash import Input, Output, State, dcc, html
import dash_leaflet as dl
import dash_leaflet.express as dlx

# Constants
radius_meters = 402.336  # Radius for station circles in meters
earth_radius = 6378137  # Earth's radius in meters
map_bounds = [[-123.0, 36.5], [-121.0, 39.0]]  # Map bounds (SW and NE corners)
operators = ['CE', 'BA', 'CT', 'AM', 'SI', 'SF', 'SA', 'SC']  # Transit operators

# Load data
with open('rail_lines.json', 'r') as f:
    rail_lines = json.load(f)
with open('stations.json', 'r') as f:
    stations = json.load(f)
with open('colors.json', 'r') as f:
    colors = json.load(f)
with open('shapes.json', 'r') as f:
    shapes = json.load(f)
with open('route_trip_ids.json', 'r') as f:
    route_trip_ids = json.load(f)

# Helper Functions
def create_circle(lat, lon, radius_meters, resolution=72):
    """Create a circular polygon around a point."""
    lat_radius = radius_meters / earth_radius * (180 / math.pi)
    lon_radius = radius_meters / (earth_radius * math.cos(math.radians(lat))) * (180 / math.pi)
    points = [
        (
            lon + lon_radius * math.cos(math.radians(angle)),
            lat + lat_radius * math.sin(math.radians(angle))
        )
        for angle in range(0, 360, int(360 / resolution))
    ]
    return Polygon(points)

# Initialize Dash App
app = dash.Dash(__name__)

# Create the outer polygon for the shaded area
outer_polygon = Polygon([
    (map_bounds[0][0], map_bounds[0][1]),  # SW
    (map_bounds[1][0], map_bounds[0][1]),  # NW
    (map_bounds[1][0], map_bounds[1][1]),  # NE
    (map_bounds[0][0], map_bounds[1][1]),  # SE
    (map_bounds[0][0], map_bounds[0][1])   # Back to SW
])

# Station data processing for the map
station_markers = []
circle_shapes = []
polylines = []

for operator in operators:
    if operator not in stations or operator not in rail_lines:
        continue

    for line_id, line_stations in stations[operator].items():
        # Process stations
        for stop in line_stations["Contents"]["dataObjects"]["ScheduledStopPoint"]:
            lat, lon = float(stop["Location"]["Latitude"]), float(stop["Location"]["Longitude"])
            station_markers.append(
                dl.Marker(
                    id=f"station-{operator}-{line_id}-{stop['id']}",
                    position=(lat, lon),
                    children=dl.Tooltip(stop["Name"]),
                )
            )
            circle_shapes.append(create_circle(lat, lon, radius_meters))
        
        # Process lines
        if line_id in rail_lines[operator]:
            line_coords = [
                (coord[1], coord[0])  # Flip lat/lon for Dash Leaflet
                for coord in rail_lines[operator][line_id]
            ]
            polylines.append(
                dl.Polyline(
                    positions=line_coords,
                    color=colors.get(line_id, "blue"),
                    weight=3
                )
            )

# Create initial shaded area
merged_circles = unary_union(circle_shapes)
shaded_area = outer_polygon.difference(merged_circles)
geojson_data = mapping(shaded_area)

# Layout
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        dl.LayerGroup(
            id="station-layer",
            children=station_markers,
        ),
        dl.LayerGroup(
            id="line-layer",
            children=polylines,
        ),
        dl.GeoJSON(
            id="shaded-layer",
            data=geojson_data,
            options=dict(style=dict(fillColor="#000", fillOpacity=0.6, color="none"))
        )
    ],
        id="map",
        center=[37.65077186632317, -122.24094250022335],
        zoom=9,
        style={'width': '100%', 'height': '600px'}
    ),
    dcc.Store(id="selected-station", data=None),  # To store selected station data
])

# Callbacks
@app.callback(
    Output("shaded-layer", "data"),
    Input("station-layer", "click_feature"),
)
def update_shaded_area(click_feature):
    if not click_feature:
        return mapping(shaded_area)  # Show full shaded area by default

    # Get clicked station coordinates
    coords = click_feature["geometry"]["coordinates"]
    lon, lat = coords
    circle = create_circle(lat, lon, radius_meters)
    new_shaded_area = outer_polygon.difference(circle)
    return mapping(new_shaded_area)

if __name__ == "__main__":
    app.run_server(debug=True)
