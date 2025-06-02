import json
import math
import dotenv
import os
from utils import makeBeautifyIcon
from folium.plugins import LocateControl, Draw, MeasureControl
from shapely.geometry import Polygon, mapping
from shapely.ops import unary_union
from folium import Element, GeoJson, Popup, GeoJsonTooltip, Marker, PolyLine, FeatureGroup, LayerControl, Map, TileLayer
import os
from PIL import Image 
from bs4 import BeautifulSoup
from xyzservices import TileProvider
from location_test import add_location_circle2 as add_location_circle

dotenv.load_dotenv()


bart_muni_stations = {
    "EMBR": {
        "lines": [
            "Red",
            "Yellow",
            "Green",
            "Blue",
            "J",
            "K",
            "L",
            "M",
            "N",
        ], # Metro Embarcadero Station, Metro Embarcadero Station == EMBR
        "other_names": [
            "Metro Embarcadero Station",
        ],
        "name": "Embarcadero"
    },
    "MONT": {
        "lines": [
            "Red",
            "Yellow",
            "Green",
            "Blue",
            "J",
            "K",
            "L",
            "M",
            "N",
        ], # Metro Montgomery Station/Outbound, Metro Montgomery Station/Downtown == MONT
        "other_names": [
            "Metro Montgomery Station/Outbound",
            "Metro Montgomery Station/Downtown",
        ],
        "name": "Montgomery"
    },
    "POWL": {
        "lines": [
            "Red",
            "Yellow",
            "Green",
            "Blue",
            "J",
            "K",
            "L",
            "M",
            "N",
        ], # Metro Powell Station/Downtown, Metro Powell Station/Outbound == POWL
        "other_names": [
            "Metro Powell Station/Downtown",
            "Metro Powell Station/Outbound",
        ],
        "name": "Powell Street"
    },
    "CIVC": {
        "lines": [
            "Red",
            "Yellow",
            "Green",
            "Blue",
            "J",
            "K",
            "L",
            "M",
            "N",
        ],# Metro Civic Center Station/Outbd, Metro Civic Center Station/Downtn == CIVC
        "other_names": [
            "Metro Civic Center Station/Outbd",
            "Metro Civic Center Station/Downtn",
        ],
        "name": "Civic Center"
    },
    # "BALB": {
    #     "lines": [
    #         "Red-N",
    #         "Yellow-N",
    #         "Green-N",
    #         "Blue-N",
    #         "J",
    #         "K",
    #     ], # Metro Balboa Park Station/Outbound, Metro Balboa Park Station/Downtown == BALB
    #     "other_names": [
    #         "Balboa Park BART/Mezzanine Level",
    #     ]
    # },
    }

combine_stations = {
    "Metro Castro Station": {
        "lines": [
            "K",
            "L",
            "M",
            "F"
        ],
        "other_names": [
            "Castro Station",
            "17th St & Castro St"
        ]
    }
}

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
ignored_lines = ["005R", "014R", "028R", "009R", "FBUS"]
ignored_stops = ["Van Ness Station Outbound"]

# Train operators
operators = ['CE', 'BA', 'CT', 'AM', 'SI', 'SF', 'SA', 'SC'] # SI maybe, its for the airport

# Cable car abbreviations converter (or what is turned in in case its not a cable car)
cable_car_to_name = lambda x: "Powell-Hyde Cable Car" if x == "PH" else "Powell-Mason Cable Car" if x == "PM" else "California Cable Car" if x == "CA" else x

def add_tiles(m:Map):
    # Add tile options
    # OpenStreetMap
    TileLayer('openstreetmap', show=False).add_to(m)
    # CartoDB Voyager
    TileLayer('cartodbvoyager', show=False).add_to(m)
    # CartoDB Dark Matter
    TileLayer('cartodbdark_matter', show=False).add_to(m)
    # Esri World Imagery
    TileLayer('esriworldimagery', show=False).add_to(m)
    # JAWG Dark
    # API Key for JAWG: ESd8imo0KmtipTKSQYSSN2Tvnu2LljJPeTnVaqVXRf84Zt378nCGRPhsqxIosl88
    jdark = TileProvider(
        name="JAWG Dark",
        url="https://tile.jawg.io/jawg-dark/{z}/{x}/{y}.png?api-key="+os.getenv("JAWG_KEY"),
        attribution="JAWG Dark",
        accessToken="ESd8imo0KmtipTKSQYSSN2Tvnu2LljJPeTnVaqVXRf84Zt378nCGRPhsqxIosl88",
    )

    TileLayer(jdark, show=False).add_to(m)
    return m

def add_sf_boundary(m:Map, test=False, name="San Francisco County Boundary"):
    # Load SF boundary data
    with open('data/borders/sf.geojson') as f:
        sf_boundary = json.load(f)

    if test:
        # Create a FeatureGroup for the boundary
        boundary_fg = FeatureGroup(name)

    # Add the boundary to the map
    sf_geojson = GeoJson(
        sf_boundary,
        style_function=lambda feature: {
            'color': '#FF0000',   # Red boundary line
            'weight': 5,          # Line thickness
        },
        name=name,
    )
    if test:
        boundary_fg.add_child(sf_geojson)
        m.add_child(boundary_fg)
    else:
        sf_geojson.add_to(m)


# Define bounds for the map (adjust northern boundary to raise the rectangle)
def create_outer_polygon(shaded_area_bounds: list):
    return Polygon([
        (shaded_area_bounds[0][0], shaded_area_bounds[0][1]),  # SW corner
        (shaded_area_bounds[1][0], shaded_area_bounds[0][1]),  # NW corner
        (shaded_area_bounds[1][0], shaded_area_bounds[1][1]),  # NE corner
        (shaded_area_bounds[0][0], shaded_area_bounds[1][1]),  # SE corner
        (shaded_area_bounds[0][0], shaded_area_bounds[0][1]),  # Back to SW corner
    ])


default_shaded_area_bounds = [
    [-123.0, 36.5],  # Southwest corner (lon, lat)
    [-121.0, 39.0],  # Northeast corner (lon, lat)
]


# Constants
radius_meters = 402.336  # Circle radius in meters (1/4 mile)
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



def add_stations(m:Map, shaded_area:bool=False, test=False, ignored_stops: list = []):
    """If shaded_area is True, return the circle shapes for the shaded area"""
    # Load colors from file
    with open('data/colors.json', 'r') as f:
        colors = json.loads(f.read())

    # Load stations from file
    with open('data/train_bus/stations.json', 'r') as f:
        stations = json.loads(f.read())
        
    with open("data/stations/stations_bart.json", "r") as f:
        old_bart_data = json.load(f)

    with open("data/stations/stations_muni.json", "r") as f:
        old_muni_data = json.load(f)

    with open("data/stations/stations_ct.json", "r") as f:
        old_ct_data = json.load(f)

    with open("data/stations/stations_vta.json", "r") as f:
        old_vta_data = json.load(f)

    with open("data/stations/stations_sfo.json", "r") as f:
        old_sfo_data = json.load(f)

    if test:
        # Create a FeatureGroup for the station circles
        stations_fg = FeatureGroup(name="Stations")
    else:
        # Create a FeatureGroup for the stations
        stations_fg = FeatureGroup(name="Station Circles")

    circle_shapes = []
    for op in operators:
        if op in ['BA', 'SF', 'CT', 'SC', 'SI']: continue
        for line_id in stations[op]:
            for stop in stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
                # Check if the stop is in ignored_stops
                if stop["Name"] in ignored_stops:
                    continue
                lat = float(stop["Location"]["Latitude"])
                lon = float(stop["Location"]["Longitude"])
                # marker = ipyleaflet.Marker(location=(lat, lon), draggable=False)
                # m.add_layer(marker)
                html = f"""<span style="background-color: {colors[op][line_id]}; color: {"white" if line_id in ["CC", "ACETrain", "SMART"] else "black"}";>{line_id}</span>, """
                html = html[:-2]
                html += "</p>"

                p = Popup(
                    f"<p><b>Station</b>: {stop['Name']}</p><!--br style='content: \" \";'--><p><b>Line</b>: {html}</p><!--br style='content: \" \";'--><p><b>Operator</b>: {op_to_name(op)}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{op}/{line_id}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
                    max_width=265
                )
                Marker(
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
                    ),
                    # TESTING (edited folium Maker class)
                    name=f"{op_to_name(op)} {line_id}",
                    operator=op,
                    line=line_id
                    # line=f"{line_id}"
                ).add_to(stations_fg)
                    
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

    def make_popup(stop):
        white_text_lines = ["L", "M", "N", "38R", "T", "Red", "Express", "Red Line"]
        line_type = lambda x: "Bus" if x == "38R" else "Line"
        html = ""
        for connection in stop["connections"]:
            if connection in ["J", "K", "L", "M", "N"]:
                html += f"""<span style="background-color: {colors["SF"][connection]}; color: {"white" if connection in white_text_lines else "black"}";>{connection} {line_type(connection)}</span>, """

    # BA
    for stop in old_bart_data:
        # Check if the stop is in ignored_stops
        if stop["Name"] in ignored_stops:
            continue
        lat = float(stop["Location"]["Latitude"])
        lon = float(stop["Location"]["Longitude"])
        html = ""
        for connection in stop["connections"]:
            if connection in ["J", "K", "L", "M", "N"]: # MUNI
                html += f"""<span style="background-color: {colors["SF"][connection]}; color: {"white" if connection in ["L", "M", "N", "38R", "T"] else "black"}";>{connection} {"Bus" if connection == "38R" else "Line"}</span>, """
            else:
                # if "Line" in connection:
                #     print(connection)
                #     connection = connection.replace(" Line", "")
                # Check for keyerror
                if f"{connection}-N" not in colors["BA"]:
                    # It could be the airtrain (SI), caltrain (CT), VTA (SC)
                    if connection in ["Limited","South County","Local Weekday","Local Weekend","Express"]: the_op = "CT"
                    if connection in ["Red Line", "Blue Line", "Red Line AirTrain", "Blue Line AirTrain"]: the_op = "SI"
                    if connection in ["Orange Line"]: the_op = "SC"
                    connection_str = connection
                else:
                    the_op = "BA"
                    connection_str = f"{connection}-N"
                html += f"""<span style="background-color: {colors[the_op][connection_str]}; color: {"white" if connection == "Red" else "black"}";>{connection}</span>, """
        html = html[:-2]

        p = Popup(
            f"<p><b>Station</b>: {stop['Name']}</p><!--br style='content: \" \";'--><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><!--br style='content: \" \";'--><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}-N/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
            max_width=265
        )

        Marker(
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
            ),
            # TESTING (edited folium Maker class)
            name=f"{op_to_name(stop['operator'])} {stop['connections'][0]}",
            line=f"{op_to_name(stop['operator'])} {stop['connections'][0]}",
            operator=stop['operator']
        ).add_to(stations_fg)
        circle = create_circle(lat, lon, radius_meters)
        circle_shapes.append(circle)

    # SF
    added_stops = []
    for stop in old_muni_data:
        # Check if the stop is in ignored_stops
        if stop["Name"] in ignored_stops:
            continue
        # print(stop['Name'])
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
            old_stop = next((old_stop for old_stop in old_muni_data if (old_stop["Name"] == stop["Name"]) and (old_stop["Location"]["Latitude"] != stop["Location"]["Latitude"] or old_stop["Location"]["Longitude"] != stop["Location"]["Longitude"])), None)
            if old_stop is None:
                lat = float(stop["Location"]["Latitude"])
                lon = float(stop["Location"]["Longitude"])
            else:
                if 'added' in old_stop and old_stop['added']:
                    continue
                old_stop['added'] = True
                lat = (float(stop["Location"]["Latitude"]) + float(old_stop["Location"]["Latitude"])) / 2
                lon = (float(stop["Location"]["Longitude"]) + float(old_stop["Location"]["Longitude"])) / 2

        else:
            lat = float(stop["Location"]["Latitude"])
            lon = float(stop["Location"]["Longitude"])
        html = ""
        if stop["Name"] == "The Embarcadero & Stockton St":
            # for i in range(10):
                # print("Found STOCKTON!")
            # print(lat)
            # print(lon)
            pass
        for connection in stop["connections"]:
            if connection == "FBUS": continue
            # print(connection)
            html += f"""<span style="background-color: {colors["SF"][connection]}; color: {"white" if connection in ["L", "M", "N", "38R", "T"] else "black"}";>{connection} {"Bus" if connection == "38R" else "Line"}</span>, """
        html = html[:-2]

        p = Popup(
            f"<p><b>Station</b>: {stop['Name']}</p><!--br style='content: \" \";'--><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><!--br style='content: \" \";'--><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
            max_width=265
        )

        Marker(
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
            ),
            # TESTING (edited folium Maker class)
            name=stop["Name"],
            line=f"{op_to_name(stop['operator'])} {stop['connections'][0]}",
            operator=stop['operator']
        ).add_to(stations_fg)
        stop['added'] = True
        circle = create_circle(lat, lon, radius_meters)
        circle_shapes.append(circle)

    # CT
    for stop in old_ct_data:
        # Check if the stop is in ignored_stops
        if stop["Name"] in ignored_stops:
            continue

        # Sort connections alphabetically
        stop["connections"].sort()
        if test == True:
            if "San Francisco Caltrain Station" in stop['Name'] and "South " not in stop['Name']:
                # Drop the southbound or northbound part of the name
                stop['Name'] = "San Francisco Caltrain Station"
                # 37.776369,-122.3949635
                stop['Location']['Latitude'] = "37.776369"
                stop['Location']['Longitude'] = "-122.3949635"
                # print("Changing San Francisco Caltrain Station")
            if "22nd Street Caltrain Station" in stop['Name']:
                # Drop the southbound or northbound part of the name
                stop['Name'] = "22nd Street Caltrain Station"
                # 37.748, -122.392
                stop['Location']['Latitude'] = "37.757583"
                stop['Location']['Longitude'] = "-122.392404"
                # print("Changing 22nd Street Caltrain Station")
            if "Bayshore Caltrain Station" in stop['Name']:
                # Drop the southbound or northbound part of the name
                stop['Name'] = "Bayshore Caltrain Station"
                # 37.70766948153158, -122.40184374398838
                stop['Location']['Latitude'] = "37.70766948153158"
                stop['Location']['Longitude'] = "-122.40184374398838"
                # print("Changing Bayshore Caltrain Station")

        lat = float(stop["Location"]["Latitude"])
        lon = float(stop["Location"]["Longitude"])
        html = f""
        for connection in stop["connections"]:
            if connection in ["Red", "Yellow"]:
                the_op = "BA"
            elif connection in ["Orange Line", "Green Line", "Blue Line"]:
                the_op = "SC"
            elif connection == "ACETrain":
                the_op = "CE"
            elif connection == "CC":
                the_op = "AM"
            else:
                the_op = "CT"
            # print(stop['operator'])
            html += f"""<span style="background-color: {colors[the_op][connection + ("-N" if connection in ['Red', 'Yellow'] else '')]}; color: {"white" if connection in ["Express"] else "black"}";>{connection.replace("Weekday", "WD").replace("Weekend", "WE")}</span>, """
        html = html[:-2]
        p = Popup(
            f"<p><b>Station</b>: {stop['Name']}</p><!--br style='content: \" \";'--><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><!--br style='content: \" \";'--><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
            max_width=265
        )

        Marker(
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
            ),
            # TESTING (edited folium Maker class)
            name=f"{op_to_name(stop['operator'])} {stop['connections'][0]}",
            line=f"{op_to_name(stop['operator'])} {stop['connections'][0]}",
            operator=stop['operator']
        ).add_to(stations_fg)
        circle = create_circle(lat, lon, radius_meters)
        circle_shapes.append(circle)

    # FIXME: Consolidate VTA stops and update all maps!!!
    for stop in old_vta_data:
        # Check if the stop is in ignored_stops
        if stop["Name"] in ignored_stops:
            continue

        lat = float(stop["Location"]["Latitude"])
        lon = float(stop["Location"]["Longitude"])
        html = ""
        for connection in stop["connections"]:
            html += f"""<span style="background-color: {colors["SC"][connection]}; color: {"white" if connection in ["Express"] else "black"}";>{connection}</span>, """
        html = html[:-2]

        p = Popup(
            f"<p><b>Station</b>: {stop['Name']}</p><!--br style='content: \" \";'--><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><!--br style='content: \" \";'--><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
            max_width=265
        )

        Marker(
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
            ),
            # TESTING (edited folium Maker class)
            name=f"{op_to_name(stop['operator'])} {stop['connections'][0]}",
            line=f"{op_to_name(stop['operator'])} {stop['connections'][0]}",
            operator=stop['operator']
        ).add_to(stations_fg)
        circle = create_circle(lat, lon, radius_meters)
        circle_shapes.append(circle)


    for stop in old_sfo_data:
        # Check if the stop is in ignored_stops
        if stop["Name"] in ignored_stops:
            continue

        lat = float(stop["Location"]["Latitude"])
        lon = float(stop["Location"]["Longitude"])
        html = ""
        for connection in stop["connections"]:
            # If the connection is not in colors, loop through the color keys and values and look through the keys of the value and check if the connection is in the value
            # if connection not in colors["SI"]:
            #     for op, raw_colors in colors.items():
            #         # Loop through the raw_colors and check if the connection is in the value
            #         for actual_color, color_value in raw_colors.items():
            #             if connection in actual_color:
            #                 # print(f"Found {connection} in {op} {actual_color}")
            #                 html += f"""<span style="background-color: {color_value}; color: {"white" if connection in ["Red Line"] else "black"}";>{connection}</span>, """
            #                 break
            if connection not in colors["SI"]:
                # The only connection that is not in colors["SI"] is anything to do with BART so just change the operator to BA
                the_op = "BA"
            else:
                the_op = "SI"
            html += f"""<span style="background-color: {colors[the_op][connection]}; color: {"white" if connection in ["Red Line", "Red"] else "black"}";>{connection}</span>, """
        html = html[:-2]

        p = Popup(
            f"<p><b>Station</b>: {stop['Name']}</p><!--br style='content: \" \";'--><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><!--br style='content: \" \";'--><p><b>Operator</b>: {op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
            max_width=265
        )

        Marker(
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
            ),
            # TESTING (edited folium Maker class)
            name=f"{op_to_name(stop['operator'])} {stop['connections'][0]}",
            line=f"{op_to_name(stop['operator'])} {stop['connections'][0]}",
            operator=stop['operator']
        ).add_to(stations_fg)
        circle = create_circle(lat, lon, radius_meters)
        circle_shapes.append(circle)

    # Add the station circles to the map
    m.add_child(stations_fg)

    if shaded_area:
        return circle_shapes



def add_lines(m:Map):
    with open('data/colors.json', 'r') as f:
        colors = json.loads(f.read())

    with open('data/train_bus/shapes.json', 'r') as f:
        shapes = json.loads(f.read())

    with open('data/train_bus/route_trip_ids.json', 'r') as f:
        route_trip_ids = json.loads(f.read())

    # Draw lines from caltrain.geojson
    with open('data/lines/caltrain.geojson', 'r') as f:
        caltrain_geojson = json.load(f)

    # Draw lines from filtered_muni_routes.geojson
    with open('data/lines/filtered_muni_routes_bus.geojson', 'r') as f:
        muni_geojson = json.load(f)

    with open("data/lines/ace.geojson", "r") as f:
        ace_geojson = json.load(f)

    caltrain_fg = FeatureGroup(name="Caltrain")
    ace_fg = FeatureGroup(name="ACE")
    other_fg = FeatureGroup(name="Other")


    for op in operators:
        if op not in shapes:
            continue

        # Skip Muni (Drawn later and better)
        if op == 'SF':
            # print("Skipping Muni, drawn later")
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
                # print(f"Skipping Caltrain, testing new way of drawing lines")
                continue
            coords = []
            for pos in shapes[op][line_id]:
                # print(pos)
                coords.append((pos[0], pos[1]))
            PolyLine(
                coords, 
                color=route_trip_ids[op][route]['color'], 
                #tooltip=f"{op} {rti} {line_id}"
                tooltip=f"{op_to_name(op)} {rti}",
                name=f"{op_to_name(op)} {rti}"
            ).add_to(other_fg)


    GeoJson(
        caltrain_geojson,
        style_function=lambda feature: {
            'color': '#FF0000',   # Red boundary line
            'weight': 5,          # Line thickness
        },
        tooltip="Caltrain",
        name="Caltrain",
        smooth_factor=0.1
    ).add_to(caltrain_fg)

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

        
        # print(f"Adding Muni {cable_car_to_name(lineabbr)} to map...")
        # print(f"Color: {color}")
        # Create a new GeoJSON object for each line
        muni_geo = GeoJson(
            {
                "type": "FeatureCollection",
                "features": [feature]
            },
            style_function=lambda feature, color=color, weight=weight: {
                'color': color,
                'weight': weight,
            },
            tooltip=GeoJsonTooltip(
                fields=['lineabbr', 'service_ca'],  # Tooltip fields from GeoJSON 'properties'
                aliases=['Name:', 'Type:'],  # Display aliases
            ),
            smooth_factor=0.1,
            name=f"MUNI {cable_car_to_name(lineabbr)}",
        )

        # Check if the line is in the muni_layers dictionary
        
        if lineabbr not in muni_layers:        
            # Create a new featureGroup
            muni_layers[lineabbr] = FeatureGroup(name=f"MUNI {cable_car_to_name(lineabbr)}")

        # Add the geojson to the featureGroup
        muni_layers[lineabbr].add_child(muni_geo)

    # Add the featureGroups to the map
    for lineabbr in muni_layers:
        m.add_child(muni_layers[lineabbr])

    # Add the ACE lines to the map
    GeoJson(
        ace_geojson,
        style_function=lambda feature, color=colors['CE']['ACETrain']: {
            'color': color,
            'weight': 4,
        },
        tooltip="ACE",
        name="ACE",
        smooth_factor=0.1
    ).add_to(ace_fg)

    # Add the featureGroups to the map
    m.add_child(caltrain_fg)
    m.add_child(ace_fg)
    m.add_child(other_fg)

def add_lines2(m:Map):
    # Load data from files
    with open('data/colors.json', 'r') as f:
        colors = json.loads(f.read())

    # BART
    with open('data/track_data/bart/bart_blue.geojson', 'r') as f:
        bart_blue_geojson = json.load(f)
    with open('data/track_data/bart/bart_green.geojson', 'r') as f:
        bart_green_geojson = json.load(f)
    with open('data/track_data/bart/bart_orange.geojson', 'r') as f:
        bart_orange_geojson = json.load(f)
    with open('data/track_data/bart/bart_red.geojson', 'r') as f:
        bart_red_geojson = json.load(f)
    with open('data/track_data/bart/bart_yellow.geojson', 'r') as f:
        bart_yellow_geojson = json.load(f)
    with open('data/track_data/oak_connector.geojson', 'r') as f:
        bart_oak_geojson = json.load(f)
    
    bart_lines = {'Blue': bart_blue_geojson, 'Green': bart_green_geojson, 'Orange': bart_orange_geojson, 'Red': bart_red_geojson, 'Yellow': bart_yellow_geojson, 'Beige': bart_oak_geojson}

    # Muni lines
    with open('data/track_data/muni_f.geojson', 'r') as f:
        muni_f_geojson = json.load(f)
    with open('data/track_data/muni_j.geojson', 'r') as f:
        muni_j_geojson = json.load(f)
    with open('data/track_data/muni_k.geojson', 'r') as f:
        muni_k_geojson = json.load(f)
    with open('data/track_data/muni_l.geojson', 'r') as f:
        muni_l_geojson = json.load(f)
    with open('data/track_data/muni_m.geojson', 'r') as f:
        muni_m_geojson = json.load(f)
    with open('data/track_data/muni_n.geojson', 'r') as f:
        muni_n_geojson = json.load(f)
    with open('data/track_data/t_line_fixed.geojson', 'r') as f:
        muni_t_geojson = json.load(f)
    with open('data/track_data/muni_38R.geojson', 'r') as f:
        muni_38R_geojson = json.load(f)
    # Cable cars
    with open('data/track_data/california_cable_car.geojson', 'r') as f:
        california_cable_car_geojson = json.load(f)
    with open('data/track_data/powell_hyde_cable_car.geojson', 'r') as f:
        powell_hyde_cable_car_geojson = json.load(f)
    with open('data/track_data/powell_mason_cable_car.geojson', 'r') as f:
        powell_mason_cable_car_geojson = json.load(f)

    muni_lines = {'F': muni_f_geojson, 'J': muni_j_geojson, 'K': muni_k_geojson, 'L': muni_l_geojson, 'M': muni_m_geojson, 'N': muni_n_geojson, 'T': muni_t_geojson, '038R': muni_38R_geojson, 'CA': california_cable_car_geojson, 'PH': powell_hyde_cable_car_geojson, 'PM': powell_mason_cable_car_geojson}
    
    # Caltrain
    with open('data/track_data/caltrain.geojson', 'r') as f:
        caltrain_geojson = json.load(f)
    
    # ACE
    with open('data/track_data/ace.geojson', 'r') as f:
        ace_geojson = json.load(f)

    # Other
    with open('data/train_bus/shapes.json', 'r') as f:
        shapes = json.loads(f.read())

    with open('data/train_bus/route_trip_ids.json', 'r') as f:
        route_trip_ids = json.loads(f.read())

    # Add lines to map (dont use GeoJson, add with PolyLine)
    for op in operators:
        if op in ["BA", "SF", "CE"]: continue
        if op not in shapes:
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
                # print(f"Skipping Caltrain, testing new way of drawing lines")
                continue
            if rti in ["5R", "9R", "14R", "28R"]: continue
            coords = []
            for pos in shapes[op][line_id]:
                # print(pos)
                coords.append((pos[0], pos[1]))
            PolyLine(
                coords, 
                color=route_trip_ids[op][route]['color'], 
                #tooltip=f"{op} {rti} {line_id}"
                tooltip=f"{op_to_name(op)} {rti}",
                name=f"{op_to_name(op)} {rti}",
                weight=3,
                # TESTING (edited folium PolyLine class)
                operator=op,
                line=line_id
            ).add_to(m)

    # Add BART lines to map
    for color, geojson in bart_lines.items():
        for feature in geojson['features']:
            coords = feature['geometry']['coordinates']
            # tooltip=GeoJsonTooltip(
            #     fields=['lineabbr', 'service_ca'],  # Tooltip fields from GeoJSON 'properties'
            #     aliases=['Name:', 'Type:'],  # Display aliases
            # ),
            PolyLine(
                coords,
                color=colors['BA'][color+"-N"],
                tooltip=f"BART {color}",
                name=f"BART {color}",
                weight=4,
                # TESTING (edited folium PolyLine class)
                operator="BA",
                line=color
            ).add_to(m)

    # Add Muni lines to map
    for color, geojson in muni_lines.items():
        for feature in geojson['features']:
            coords = feature['geometry']['coordinates']
            PolyLine(
                coords,
                color=colors['SF'][color],
                tooltip=f"Muni {cable_car_to_name(color)}",
                name=f"Muni {cable_car_to_name(color)}",
                weight=3 if hasattr(feature['properties'], 'railway') and feature['properties']['railway'] == "light_rail" else 2,
                # TESTING (edited folium PolyLine class)
                operator="SF",
                line=color
            ).add_to(m)

    # Add Caltrain lines to map
    for feature in caltrain_geojson['features']:
        coords = feature['geometry']['coordinates']
        PolyLine(
            coords,
            color='#FF0000',
            tooltip="Caltrain",
            name="Caltrain",
            weight=5,
            # TESTING (edited folium PolyLine class)
            operator="CT",
            line="Caltrain"
        ).add_to(m)

    # Add ACE lines to map
    for feature in ace_geojson['features']:
        coords = feature['geometry']['coordinates']
        PolyLine(
            coords,
            color=colors['CE']['ACETrain'],
            tooltip="ACE",
            name="ACE",
            weight=4,
            # TESTING (edited folium PolyLine class)
            operator="CE",
            line="ACE"
        ).add_to(m)




def add_shaded_region(m, circle_shapes, outer_polygon, keep_in_front=True):
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
    gjson = GeoJson(
        shaded_geojson,
        style_function=lambda x: {
            'fillColor': x['properties']['fill'],
            'fillOpacity': x['properties']['fill-opacity'],
            'color': 'none',
            'interactive': False,
        },
        name="Shaded Area"
    )
    gjson.add_to(m)
    if keep_in_front:
        m.keep_in_front(gjson)




# def add_location_circle(m, radius):
#     # JavaScript to update the circle dynamically
#     js = """
#     <script>
#     document.addEventListener("DOMContentLoaded", function() {{
#         var map = document.querySelector(".folium-map")._leaflet_map;  

#         function updateCircle(e) {{
#             if (window.userCircle) {{
#                 window.userCircle.setLatLng(e.latlng);
#             }} else {{
#                 window.userCircle = L.circle(e.latlng, {{
#                     radius: {},  // 1 mile in meters
#                     color: 'blue',
#                     fillColor: 'blue',
#                     fillOpacity: 0.2
#                 }}).addTo(map);
#             }}
#         }}

#         map.on("locationfound", updateCircle);
#     }});
#     </script>
#     """.format(radius)

#     map_find_html = """
#     <script>
#     L.Map.addInitHook(function () {
#     // Store a reference of the Leaflet map object on the map container,
#     // so that it could be retrieved from DOM selection.
#     // https://leafletjs.com/reference-1.3.4.html#map-getcontainer
#     this.getContainer()._leaflet_map = this;
#     });
#     </script>
#     """

#     # Add the map_find_html to the map
#     m.get_root().html.add_child(Element(map_find_html))
#     # Add the JS script to the map
#     m.get_root().html.add_child(Element(js))

def OLD_add_location_circle(m, radius):
    # JavaScript to update the circle dynamically within a FeatureGroup
    # js = """
    # <script>
    # document.addEventListener("DOMContentLoaded", function() {{
    #     var map = document.querySelector(".folium-map")._leaflet_map;  
    #     var locationLayer = L.featureGroup().addTo(map);  // Create FeatureGroup

    #     function updateCircle(e) {{
    #         locationLayer.clearLayers();  // Remove previous circles
    #         L.circle(e.latlng, {{
    #             radius: {},  
    #             color: 'blue',
    #             fillColor: 'blue',
    #             fillOpacity: 0.2
    #         }}).addTo(locationLayer);
    #     }}

    #     map.on("locationfound", updateCircle);
    #     L.control.layers(null, {{ "Location Radius": locationLayer }}).addTo(map);
    # }});
    # </script>
    # """.format(radius)

    # map_find_html = """
    # <script>
    # L.Map.addInitHook(function () {
    #     this.getContainer()._leaflet_map = this;
    # });
    # </script>
    # """
    # Create a FeatureGroup for the location circle
    location_layer = FeatureGroup(name="Location Radius").add_to(m)

    # JavaScript to update the circle dynamically
    js = f"""
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        var map = document.querySelector(".folium-map")._leaflet_map;  
        var locationLayer = map._layers[Object.keys(map._layers).find(k => map._layers[k].options && map._layers[k].options.name === "Location Radius")];

        function updateCircle(e) {{
            locationLayer.clearLayers();  // Remove previous circles
            L.circle(e.latlng, {{
                radius: {radius},  
                color: 'blue',
                fillColor: 'blue',
                fillOpacity: 0.2
            }}).addTo(locationLayer);
        }}

        map.on("locationfound", updateCircle);
    }});
    </script>
    """

    map_find_html = """
    <script>
    L.Map.addInitHook(function () {
        this.getContainer()._leaflet_map = this;
    });
    </script>
    """

    # Add the map_find_html to the map
    m.get_root().html.add_child(Element(map_find_html))
    # Add the JS script to the map
    m.get_root().html.add_child(Element(js))

    return location_layer

def add_plugins(m, location_circle=False, radius_meters=402.336):
    # Add location control
    m.add_child(LocateControl(strings={"title": "See you current location", "popup": "Your position"},))

    # Add location circle if true
    if location_circle:
        add_location_circle(m, radius_meters)

    # Add measure control
    m.add_child(MeasureControl())

    drawings = FeatureGroup(name="Drawings")
    drawings.add_to(m)
    Draw(
        feature_group=drawings, 
        export=True
    ).add_to(m)
    m.add_child(LayerControl())
    # NOTE: If you are ahving trouble with the LayerControl not showing up and this error in the console:
    # Uncaught TypeError: Cannot read properties of undefined (reading 'setZIndex')
    # Try adding the tile layers first before adding any other layers to the map.
    # I.E. Add them right after creating the map object.

    # m = folium.Map()
    # transit_map.add_tiles(m)
    # ...


def add_favicons(filename:str):
    # Load favicons from folder "favicons" and add them to the header
    # the_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    the_path = ""
    favicon_html = ""
    for file in os.listdir(f"{the_path}favicons"):
        if file.endswith(".png"):
            img = Image.open(f"{the_path}favicons/{file}")
            width, height = img.size

            if file == "apple-touch-icon.png":
                favicon_html += f'<link rel="apple-touch-icon" sizes="{width}x{height}" href="favicons/{file}">'
            else:
                favicon_html += f'<link rel="icon" type="image/png" sizes="{width}x{height}" href="favicons/{file}">'

    # Add site.webmanifest for PWA support (also in the favicons folder)
    favicon_html += f'<link rel="manifest" href="{the_path}/favicons/site.webmanifest">'
    
    # Add the favicon HTML to the map
    soup = BeautifulSoup(open(filename), 'html.parser')
    head = soup.find('head')
    if not head:
        # Not found, create a new head tag
        print("No <head> tag found, creating a new one.")
        head = soup.new_tag('head')
        soup.insert(0, head)
    # print(f"Found Header" if head else "No Header")
    head.append(BeautifulSoup(favicon_html, 'html.parser'))  # Needs to be parsed as html by BeautifulSoup to work.

    # Write to file
    with open(filename, "w") as f:
        f.write(str(soup))

    