import json, folium, dotenv, os
from utils import makeBeautifyIcon
import math
from folium.plugins import LocateControl, Draw
from shapely.geometry import Polygon, mapping
from shapely.ops import unary_union
from xyzservices import TileProvider
from utils.station_consolidate import bart_muni_stations
from transit_map import add_favicons

# Load the .env file
dotenv.load_dotenv()


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

with open("stations_bart.json", "r") as f:
    old_bart_data = json.load(f)

with open("stations_muni.json", "r") as f:
    old_muni_data = json.load(f)

print(len(old_muni_data))
for station in old_muni_data:
    print(f"Hi {station['Name']}", end=" ")
    # print(station['Name'])

with open("stations_ct.json", "r") as f:
    old_ct_data = json.load(f)

with open("stations_vta.json", "r") as f:
    old_vta_data = json.load(f)

with open("stations_sfo.json", "r") as f:
    old_sfo_data = json.load(f)

# Ignored lines (duplicate stations)
ignored_lines = ["005R", "014R", "028R", "009R", "FBUS"]
ignored_stops = ["Van Ness Station Outbound"]

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
# CartoDB Dark Matter
folium.TileLayer('cartodbdark_matter', show=False).add_to(m)
# Esri World Imagery
folium.TileLayer('esriworldimagery', show=False).add_to(m)
# JAWG Dark
# API Key for JAWG: ESd8imo0KmtipTKSQYSSN2Tvnu2LljJPeTnVaqVXRf84Zt378nCGRPhsqxIosl88
jdark = TileProvider(
    name="JAWG Dark",
    url="https://tile.jawg.io/jawg-dark/{z}/{x}/{y}.png?api-key="+os.getenv("JAWG_KEY"),
    attribution="JAWG Dark",
    accessToken="ESd8imo0KmtipTKSQYSSN2Tvnu2LljJPeTnVaqVXRf84Zt378nCGRPhsqxIosl88",
)

folium.TileLayer(jdark, show=False).add_to(m)

# Load rail lines from file
with open('train_bus/rail_lines.json', 'r') as f:
    rail_lines = json.loads(f.read())

# Load stations from file
with open('train_bus/stations.json', 'r') as f:
    stations = json.loads(f.read())

# Load colors from file
with open('colors.json', 'r') as f:
    colors = json.loads(f.read())


# The actual coordinates are in stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"][num]["Location"]["Latitude"]
# Add stations to map
print("Adding stations to map...")
circle_shapes = []
for op in operators:
    if op in ['BA', 'SF', 'CT', 'SC', 'SI']: continue
    for line_id in stations[op]:
        for stop in stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
            lat = float(stop["Location"]["Latitude"])
            lon = float(stop["Location"]["Longitude"])
            # marker = ipyleaflet.Marker(location=(lat, lon), draggable=False)
            # m.add_layer(marker)
            html = f"""<span style="background-color: {colors[op][line_id]}; color: {"white" if line_id in ["CC", "ACETrain", "SMART"] else "black"}";>{line_id}</span>, """
            html = html[:-2]
            html += "</p>"

            p = folium.Popup(
                f"<p><b>Station</b>: {stop['Name']}</p><br style='content: \" \";'><p><b>Line</b>: {html}</p><br style='content: \" \";'><p><b>Operator</b>: {op_to_name(op)}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{op}/{line_id}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
                max_width=265
            )
            folium.Marker(
                location=[lat, lon],
                popup=p,#stop['Name'],
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
            # folium.Circle(
            #     location=[lat, lon],
            #     radius=402.336, # 0.25 miles in meters
            #     color='#3186cc',
            #     fill=False,
            #     #fill_color='#3186cc'
            # ).add_to(station_circles_group)
            # Create a circle using the new function
            circle = create_circle(lat, lon, radius_meters)
            circle_shapes.append(circle)


# BA
for stop in old_bart_data:
    lat = float(stop["Location"]["Latitude"])
    lon = float(stop["Location"]["Longitude"])
    html = ""
    for connection in stop["connections"]:
        if connection in ["J", "K", "L", "M", "N"]: # MUNI
            html += f"""<span style="background-color: {colors["SF"][connection]}; color: {"white" if connection in ["L", "M", "N", "38R", "T"] else "black"}";>{connection} {"Bus" if connection == "38R" else "Line"}</span>, """
        else:
            html += f"""<span style="background-color: {colors["BA"][f'{connection}-N']}; color: {"white" if connection == "Red" else "black"}";>{connection}</span>, """
    html = html[:-2]

    p = folium.Popup(
        f"<p><b>Station</b>: {stop['Name']}</p><br style='content: \" \";'><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><br style='content: \" \";'><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}-N/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
        max_width=265
    )

    folium.Marker(
        location=[lat, lon],
        popup=p,#stop['Name'],
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
    circle = create_circle(lat, lon, radius_meters)
    circle_shapes.append(circle)

# SF
added_stops = []
for stop in old_muni_data:
    print(stop['Name'])
    if (stop['Name'], stop['id']) in added_stops:
        continue
    
    if stop["Name"] in ignored_stops:
        continue
    # Check if the stop is in any item in bart_muni_stations['other_names'] twice (the current stop and the old stop)
    
    if stop["Name"] in [item for sublist in [value["other_names"] for value in bart_muni_stations.values()] for item in sublist]:
        continue
    
    # Check if the stop name is the same as another stop name in the list, if so only add a point at the midpoint between the two stations
    # Remove the current stop from stop list
    # old_muni_data.remove(stop)
    added_stops.append((stop['Name'], stop['id']))
    
    if any(stop["Name"] == old_stop["Name"] for old_stop in old_muni_data):
    
        # get old station (NOT THE CURRENT ONE)
        # old_stop = next(old_stop for old_stop in old_muni_data if old_stop["Name"] == stop["Name"])
        # print(stop['Name'])
        old_stop = next((old_stop for old_stop in old_muni_data if (old_stop["Name"] == stop["Name"]) and (old_stop["Location"]["Latitude"] != stop["Location"]["Latitude"] or old_stop["Location"]["Longitude"] != stop["Location"]["Longitude"])), None)
        if old_stop is None:
            lat = float(stop["Location"]["Latitude"])
            lon = float(stop["Location"]["Longitude"])
        else:
            if 'added' in old_stop and old_stop['added']:
                continue
            old_stop['added'] = True
            # print("Found duplicate station: ", stop["Name"])
            # Get lat and lon of midpoint between the two stations
            # print(f"{stop['Location']['Latitude']} {stop['Location']['Longitude']}")
            # print(f"{old_stop['Location']['Latitude']} {old_stop['Location']['Longitude']}")
            lat = (float(stop["Location"]["Latitude"]) + float(old_stop["Location"]["Latitude"])) / 2
            lon = (float(stop["Location"]["Longitude"]) + float(old_stop["Location"]["Longitude"])) / 2

    else:
        lat = float(stop["Location"]["Latitude"])
        lon = float(stop["Location"]["Longitude"])
    html = ""
    if stop["Name"] == "The Embarcadero & Stockton St":
        for i in range(10):
            print("Found STOCKTON!")
        print(lat)
        print(lon)
    for connection in stop["connections"]:
        if connection == "FBUS": continue
        # print(connection)
        html += f"""<span style="background-color: {colors["SF"][connection]}; color: {"white" if connection in ["L", "M", "N", "38R", "T"] else "black"}";>{connection} {"Bus" if connection == "38R" else "Line"}</span>, """
    html = html[:-2]

    p = folium.Popup(
        f"<p><b>Station</b>: {stop['Name']}</p><br style='content: \" \";'><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><br style='content: \" \";'><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
        max_width=265
    )

    folium.Marker(
        location=[lat, lon],
        popup=p,#stop['Name'],
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
    stop['added'] = True
    circle = create_circle(lat, lon, radius_meters)
    circle_shapes.append(circle)


added_stops = []
for stop in old_ct_data:
    if (stop['Name'], stop['id']) in added_stops:
        continue
    # Sort connections alphabetically
    stop["connections"].sort()
    # lat = float(stop["Location"]["Latitude"])
    # lon = float(stop["Location"]["Longitude"])
    html = f""
    if any(stop["Name"] == old_stop["Name"] for old_stop in old_ct_data):
    
        # get old station (NOT THE CURRENT ONE)
        # old_stop = next(old_stop for old_stop in old_muni_data if old_stop["Name"] == stop["Name"])
        # print(stop['Name'])
        old_stop = next((old_stop for old_stop in old_ct_data if (old_stop["Name"] == stop["Name"]) and (old_stop["Location"]["Latitude"] != stop["Location"]["Latitude"] or old_stop["Location"]["Longitude"] != stop["Location"]["Longitude"])), None)
        if old_stop is None:
            lat = float(stop["Location"]["Latitude"])
            lon = float(stop["Location"]["Longitude"])
        else:
            if 'added' in old_stop and old_stop['added']:
                continue
            old_stop['added'] = True
            # print("Found duplicate station: ", stop["Name"])
            # Get lat and lon of midpoint between the two stations
            # print(f"{stop['Location']['Latitude']} {stop['Location']['Longitude']}")
            # print(f"{old_stop['Location']['Latitude']} {old_stop['Location']['Longitude']}")
            lat = (float(stop["Location"]["Latitude"]) + float(old_stop["Location"]["Latitude"])) / 2
            lon = (float(stop["Location"]["Longitude"]) + float(old_stop["Location"]["Longitude"])) / 2

    else:
        lat = float(stop["Location"]["Latitude"])
        lon = float(stop["Location"]["Longitude"])
    print(stop['Name'])
    print(stop['connections'])
    # Remove duplicates in stop["connections"]
    stop["connections"] = list(dict.fromkeys(stop["connections"]))
    for connection in stop["connections"]:
        if connection in ["Green Line", "Orange Line"]: _op = "SC"
        elif connection == "ACETrain": _op = "CE"
        elif connection == "CC": _op = "AM"
        elif connection in ["Red", "Yellow"]: _op = "BA"
        else: _op = "CT"
        html += f"""<span style="background-color: {colors[_op][(connection+"-N") if _op == "BA" else (connection)]}; color: {"white" if connection in ["Express", "CC", "ACETrain"] else "black"}";>{connection.replace("Weekday", "WD").replace("Weekend", "WE")}</span>, """
    html = html[:-2]
    p = folium.Popup(
        f"<p><b>Station</b>: {stop['Name']}</p><br style='content: \" \";'><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><br style='content: \" \";'><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
        max_width=265
    )

    folium.Marker(
        location=[lat, lon],
        popup=p,#stop['Name'],
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
    circle = create_circle(lat, lon, radius_meters)
    circle_shapes.append(circle)

for stop in old_vta_data:

    lat = float(stop["Location"]["Latitude"])
    lon = float(stop["Location"]["Longitude"])
    html = ""
    for connection in stop["connections"]:
        html += f"""<span style="background-color: {colors["SC"][connection]}; color: {"white" if connection in ["Express"] else "black"}";>{connection}</span>, """
    html = html[:-2]

    p = folium.Popup(
        f"<p><b>Station</b>: {stop['Name']}</p><br style='content: \" \";'><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><br style='content: \" \";'><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
        max_width=265
    )

    folium.Marker(
        location=[lat, lon],
        popup=p,#stop['Name'],
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
    circle = create_circle(lat, lon, radius_meters)
    circle_shapes.append(circle)


for stop in old_sfo_data:

    lat = float(stop["Location"]["Latitude"])
    lon = float(stop["Location"]["Longitude"])
    html = ""
    for connection in stop["connections"]:
        html += f"""<span style="background-color: {colors["SI"][connection]}; color: {"white" if connection in ["Red Line"] else "black"}";>{connection}</span>, """
    html = html[:-2]

    p = folium.Popup(
        f"<p><b>Station</b>: {stop['Name']}</p><br style='content: \" \";'><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><br style='content: \" \";'><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
        max_width=265
    )

    folium.Marker(
        location=[lat, lon],
        popup=p,#stop['Name'],
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

"""# Format the muni_geojson to combine the southbound and northbound lines
new_muni_geojson = {
    "type": "FeatureCollection",
    "features": []
}
for feature in muni_geojson['features']:
    # Check if the line is not in the new_muni_geojson
    if feature['properties']['lineabbr'] not in new_muni_geojson:
        new_muni_geojson[feature['properties']['lineabbr']] = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": []
            },
            "properties": {
                "lineabbr": feature['properties']['lineabbr'],
                "service_ca": feature['properties']['service_ca']
            }
        }
    # Add the coordinates to the new_muni_geojson
    new_muni_geojson[feature['properties']['lineabbr']]['geometry']['coordinates'] += feature['geometry']['coordinates']

# Set muni_geojson to the new_muni_geojson
muni_geojson = new_muni_geojson"""


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
            tooltip=f"{op_to_name(op)} {rti}",
            name=f"{op_to_name(op)} {rti}"
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
    # print(f"Color: {color}")
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

# Add the ACE lines to the map
folium.GeoJson(
    ace_geojson,
    style_function=lambda feature, color=colors['CE']['ACETrain']: {
        'color': color,
        'weight': 4,
    },
    tooltip="ACE",
    name="ACE",
    smooth_factor=0.1
).add_to(m)




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



# Add location control
m.add_child(LocateControl(strings={"title": "See you current location", "popup": "Your position"},))
# Add measure control
m.add_child(folium.plugins.MeasureControl())
drawings = folium.FeatureGroup(
    name="Drawings"
)
drawings.add_to(m)
Draw(
    feature_group=drawings, 
    export=True
).add_to(m)

# Optionally, add z-indexing manually through the map options
m.add_child(folium.LayerControl())
filename = "map_new.html"
print(f"Saving map as {filename}...")
m.save(filename)
print("Done!")
print("Adding favicons...")
# Add favicons
add_favicons(filename)
print("Done!")