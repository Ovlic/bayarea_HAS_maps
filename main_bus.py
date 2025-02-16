import json, folium
from utils import makeBeautifyIcon
import math
from folium.plugins import LocateControl
from shapely.geometry import Polygon, mapping
from shapely.ops import unary_union

def op_to_name(op):
    if op == 'CT':
        return 'Caltrain'
    if op == 'BA':
        return 'BART'
    if op == 'AM':
        return 'Capitol Corridor'
    if op == 'CE':
        return 'Altamont Corridor Express'
    if op == 'SI':
        return 'San Francisco Airport'
    if op == 'SF':
        return 'Muni'
    if op == 'SA':
        return 'SMART'
    if op == 'SC':
        return 'VTA'
    if op == "AC":
        return "AC Transit"
    return op

# Ignored lines (duplicate stations)
ignored_lines = ["005R", "014R", "028R", "009R"]

# Train operators
operators = ['CE', 'BA', 'CT', 'AM', 'SI', 'SF', 'SA', 'SC'] # SI maybe, its for the airport

# Cable car abbreviations converter (or what is turned in in case its not a cable car)
cable_car_to_name = lambda x: "Powell-Hyde Cable Car" if x == "PH" else "Powell-Mason Cable Car" if x == "PM" else "California Cable Car" if x == "CA" else x

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

# Constants
radius_meters = 402.336  # Circle radius in meters
earth_radius = 6378137  # Earth's radius in meters

# Function to generate a circle with accurate scaling for both axes
def create_circle(lat, lon, radius_meters, resolution=72):
    # Convert radius to degrees for latitude
    lat_radius = radius_meters / earth_radius * (180 / math.pi)
    
    # Adjust the radius for longitude based on the latitude
    lon_radius = radius_meters / (earth_radius * math.cos(math.radians(lat))) * (180 / math.pi)
    
    # Number of points in the circle (resolution)
    points = []
    
    # Generate points in a circle around the (lat, lon)
    for angle in range(0, 360, int(360 / resolution)):
        # Convert angle to radians
        angle_rad = math.radians(angle)
        
        # Calculate the new latitude and longitude based on the angle and radii
        new_lat = lat + lat_radius * math.sin(angle_rad)
        new_lon = lon + lon_radius * math.cos(angle_rad)
        
        # Append the new point
        points.append((new_lon, new_lat))
    
    # Create a polygon from the points
    return Polygon(points)

m = folium.Map(
    #location=[37.65077186632317, -122.24094250022335],
    #zoom_start=9,
    location=[37.7545, -122.4425],
    zoom_start=12,
    # zoom_control=False,
    # attributionControl=False,
    tiles="cartodbpositron"
    )

# Add tile options
# OpenStreetMap
folium.TileLayer('openstreetmap', show=False).add_to(m)
# CartoDB Voyager
folium.TileLayer('cartodbvoyager', show=False).add_to(m)
# Esri World Imagery
folium.TileLayer('esriworldimagery', show=False).add_to(m)
# JAWG Dark
folium.TileLayer('jawgdark', show=False).add_to(m)

# Load rail lines from file
with open('train_bus/rail_lines.json', 'r') as f:
    rail_lines = json.loads(f.read())

# Load stations from file
with open('train_bus/stations.json', 'r') as f:
    stations = json.loads(f.read())

# Load colors from file
with open('colors.json', 'r') as f:
    colors = json.loads(f.read())

station_circles_group = folium.FeatureGroup(name="Station Circles", show=True)

# The actual coordinates are in stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"][num]["Location"]["Latitude"]
# Add stations to map
print("Adding stations to map...")
circle_shapes = []
for op in operators:
    for line_id in stations[op]:
        for stop in stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
            lat = float(stop["Location"]["Latitude"])
            lon = float(stop["Location"]["Longitude"])
            # marker = ipyleaflet.Marker(location=(lat, lon), draggable=False)
            # m.add_layer(marker)
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
                
            # Add a 0.25 mile radius circle around the station
            folium.Circle(
                location=[lat, lon],
                radius=402.336, # 0.25 miles in meters
                color='#3186cc',
                fill=False,
                #fill_color='#3186cc'
            ).add_to(station_circles_group)
            # Create a circle using the new function
            circle = create_circle(lat, lon, radius_meters)
            circle_shapes.append(circle)


# https://api.511.org/transit/shapes?&operator_id=BA&trip_id=1721359

# Add lines to map
print("Adding lines to map...")
# Load shapes from file
with open('train_bus/shapes.json', 'r') as f:
    shapes = json.loads(f.read())

with open('train_bus/route_trip_ids.json', 'r') as f:
    route_trip_ids = json.loads(f.read())

# Draw lines from caltrain.geojson
with open('caltrain.geojson', 'r') as f:
    caltrain_geojson = json.load(f)

# Draw lines from filtered_muni_routes.geojson
with open('filtered_muni_routes_bus.geojson', 'r') as f:
    muni_geojson = json.load(f)

with open("ace.geojson", "r") as f:
    ace_geojson = json.load(f)


for op in operators:
    if op not in shapes:
        continue

    # Skip Muni (Drawn later and better)
    if op == 'SF':
        print("Skipping Muni, drawn later")
        continue
    
    for line_id in shapes[op]:
        # Find the route trip ID for the line
        rti = None
        for route in route_trip_ids[op]:
            # Check for empty list
            if route_trip_ids[op][route]['trip_ids'] != []:
                if route_trip_ids[op][route]['trip_ids'][0] == line_id:
                    rti = route
                    break
        
        # TESTING!!!
        if rti in ['Limited', 'Express', 'Local Weekday', 'Local Weekend']:
            print(f"Skipping Caltrain, testing new way of drawing lines")
            continue
        coords = []
        for pos in shapes[op][line_id]:
            # print(pos)
            coords.append((pos[0], pos[1]))
        folium.PolyLine(
            coords, 
            color=route_trip_ids[op][route]['color'], 
            #tooltip=f"{op} {rti} {line_id}"
            tooltip=f"{op_to_name(op)} {rti}"
        ).add_to(m)


folium.GeoJson(
    caltrain_geojson,
    style_function=lambda feature: {
        'color': '#FF0000',   # Red boundary line
        'weight': 5,          # Line thickness
    },
    tooltip="Caltrain",
    name="Caltrain",
    smooth_factor=0.1
).add_to(m)

weight_convert = lambda feature: 3 if feature['properties']['service_ca'] == "Muni Metro" else 2

muni_layers = {}
# Seperate each line in Muni
for feature in muni_geojson['features']:
    if feature['properties']['lineabbr'] in ignored_lines:
        continue
    # Get the lineabbr
    lineabbr = feature['properties']['lineabbr']
    # Get the service_ca
    service_ca = feature['properties']['service_ca']
    # Get the color from the colors.json file
    color = colors["SF"][lineabbr]
    # Get the weight
    weight = weight_convert(feature)

    
    print(f"Adding Muni {cable_car_to_name(lineabbr)} to map...")
    print(f"Color: {color}")
    # Create a new GeoJSON object for each line
    muni_geo = folium.GeoJson(
        {
            "type": "FeatureCollection",
            "features": [feature]
        },
        style_function=lambda feature, color=color, weight=weight: {
            'color': color,
            'weight': weight,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['lineabbr', 'service_ca'],  # Tooltip fields from GeoJSON 'properties'
            aliases=['Name:', 'Type:'],  # Display aliases
        ),
        smooth_factor=0.1,
        name=f"MUNI {cable_car_to_name(lineabbr)}",
    )

    # Check if the line is in the muni_layers dictionary
    
    if lineabbr not in muni_layers:        
        # Create a new featureGroup
        muni_layers[lineabbr] = folium.FeatureGroup(name=f"MUNI {cable_car_to_name(lineabbr)}")

    # Add the geojson to the featureGroup
    muni_layers[lineabbr].add_child(muni_geo)

# Add the featureGroups to the map
for lineabbr in muni_layers:
    m.add_child(muni_layers[lineabbr])




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
    },
    name="Shaded Area"
).add_to(m)
# Load San Francisco County boundary GeoJSON
with open('sf.geojson', 'r') as f:
    sf_boundary_geojson = json.load(f)

# Add the boundary to the map
folium.GeoJson(
    sf_boundary_geojson,
    style_function=lambda feature: {
        'color': '#FF0000',   # Red boundary line
        # No inner fill
        'fillOpacity': 0,
        'weight': 5,          # Line thickness
    },
    name="San Francisco County Boundary",
).add_to(m)

station_circles_group.add_to(m)

# Optionally, add z-indexing manually through the map options
m.add_child(folium.LayerControl())


# Add location control
m.add_child(LocateControl(strings={"title": "See you current location", "popup": "Your position"},))
# Add measure control
m.add_child(folium.plugins.MeasureControl())
filename = "map_bus_circles.html"
print(f"Saving map as {filename}...")
m.save(filename)
print("Done!")