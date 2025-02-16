
# Make a map for every station in "statioons.json"

import folium, json, os
from folium.plugins import LocateControl, Draw
from utils import makeBeautifyIcon

ignored_lines = ["005R", "014R", "028R", "009R"]
operators = ['CE', 'BA', 'CT', 'AM', 'SI', 'SF', 'SA', 'SC'] # SI maybe, its for the airport
cable_car_to_name = lambda x: "Powell-Hyde Cable Car" if x == "PH" else "Powell-Mason Cable Car" if x == "PM" else "California Cable Car" if x == "CA" else x

def op_to_name(op):
    if op == 'CT':
        return 'Caltrain'
    if op == 'BA':
        return 'BART'
    if op == 'AM':
        return 'CC'
    if op == 'CE':
        return 'ACE'
    if op == 'SI':
        return 'SFO'
    if op == 'SF':
        return 'Muni'
    if op == 'SA':
        return 'SMART'
    if op == 'SC':
        return 'VTA'
    if op == "AC":
        return "AC Transit"
    return op

# Load colors from file
with open('colors.json', 'r') as f:
    colors = json.loads(f.read())

# Load the data from the file
path = 'train_bus/stations.json'
print("Loading data from", path)
with open(path) as f:
    data = json.load(f)
print("Data loaded")

with open("stations_bart.json", "r") as f:
    old_bart_data = json.load(f)

with open("stations_muni.json", "r") as f:
    old_muni_data = json.load(f)

with open("stations_ct.json", "r") as f:
    old_ct_data = json.load(f)

with open("stations_vta.json", "r") as f:
    old_vta_data = json.load(f)

with open("stations_sfo.json", "r") as f:
    old_sfo_data = json.load(f)

new_data = {}

print("Restructuring data")
print(len(data))
for operator, __data in data.items():
    if operator not in new_data:
        new_data[operator] = {}
    for line, _data in __data.items():
        if operator == "BA" and "-S" in line:
            continue
        if line not in new_data[operator]:
            new_data[operator][line] = []
        for station in _data['Contents']['dataObjects']['ScheduledStopPoint']:
            new_data[operator][line].append(station)

print("Data restructured")

# Load shapes from file
print("Loading lines from file")
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
print("Lines loaded")

def add_lines(m):
    # Add lines to map
    #print("Adding lines to map...")

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

        
        # print(f"Adding Muni {cable_car_to_name(lineabbr)} to map...")
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

    # Add ACE to map
    folium.GeoJson(
        ace_geojson,
        style_function=lambda feature: {
            'color': colors['CE']['ACETrain'],
            # 'weight': 5,          # Line thickness
        },
        tooltip="Altamont Corridor Express",
        name="Altamont Corridor Express",
        smooth_factor=0.1
    ).add_to(m)

    return m

def add_stations(m, the_station):
    # the_station is the station that shouldnt be added (because it is the center of the map and we add it later)
    for op in operators:
        if op in ["BA", "SF", "CT", "SC", "SI"]: continue
        for line_id in data[op]:
            html = ""
            if operator == "BA":
                # Test connections in popup
                # Get the station in the "bart_data" list with same station id as "station"
                old_station = next(old_station for old_station in old_bart_data if old_station["id"] == station["id"])
                html = f"<p>Connections: "
                for connection in old_station["connections"]:
                    html += f"""<span style="color: {colors["BA"][f'{connection}-N']}">{connection}</span>, """
                html += "</p>"
            
            for stop in data[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
                if stop["id"] == the_station["id"]:
                    continue
                lat = float(stop["Location"]["Latitude"])
                lon = float(stop["Location"]["Longitude"])

                html = f"""<span style="background-color: {colors[op][line_id]}; color: {"white" if line_id in ["CC", "ACETrain", "SMART"] else "black"}";>{line_id}</span>, """
                html = html[:-2]
                html += "</p>"

                p = folium.Popup(
                    f"<p><b>Station</b>: {stop['Name']}</p><br style='content: \" \";'><p><b>Line</b>: {html}</p><br style='content: \" \";'><p><b>Operator</b>: {op_to_name(op)}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{op}/{line_id}/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
                    max_width=265
                )
                # p = folium.Popup(
                #     f"<p>Station: {stop['Name']}</p><br style='content: \" \";'><p>Line: {line_id if op != "BA" else line_id[:-2]}</p><br style='content: \" \";'><p>Operator: {op_to_name(op)}</p>{html if op == 'BA' else ''}<a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{op}/{line_id.replace(' ', '')}/{stop['id'].replace(' ', '_')}.html'>View Station Map</a>",
                #     max_width=265
                # )

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

    # BA
    for stop in old_bart_data:
        if stop["id"] == the_station["id"]:
            continue
        lat = float(stop["Location"]["Latitude"])
        lon = float(stop["Location"]["Longitude"])
        html = ""
        for connection in stop["connections"]:
            html += f"""<span style="background-color: {colors["BA"][f'{connection}-N']}; color: {"white" if connection == "Red" else "black"}";>{connection}</span>, """
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

    # SF
    for stop in old_muni_data:
        if stop["id"] == the_station["id"]:
            continue
        lat = float(stop["Location"]["Latitude"])
        lon = float(stop["Location"]["Longitude"])
        html = ""
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

    for stop in old_ct_data:
        if stop["id"] == the_station["id"]:
            continue
        # Sort connections alphabetically
        stop["connections"].sort()
        lat = float(stop["Location"]["Latitude"])
        lon = float(stop["Location"]["Longitude"])
        html = f""
        for connection in stop["connections"]:
            html += f"""<span style="background-color: {colors["CT"][connection]}; color: {"white" if connection in ["Express"] else "black"}";>{connection.replace("Weekday", "WD").replace("Weekend", "WE")}</span>, """
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

    for stop in old_vta_data:
        if stop["id"] == the_station["id"]:
            continue
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


    for stop in old_sfo_data:
        if stop["id"] == the_station["id"]:
            continue
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

    
    


for operator, __data in new_data.items():
    print(f"Operator: {operator}")
    for line, stations in __data.items():
        print(f"Line: {line}")
        for station in stations:
            filename = f"{station['id'].replace(' ', '_')}.html"
            # Create a map centered on the station
            m = folium.Map(
                location=[station['Location']['Latitude'], station['Location']['Longitude']], 
                zoom_start=15,
                tiles="cartodbpositron"
            )

            # Add tile options
            # OpenStreetMap
            folium.TileLayer('openstreetmap', show=False).add_to(m)
            # CartoDB Voyager
            folium.TileLayer('cartodbvoyager', show=False).add_to(m)
            # Esri World Imagery
            folium.TileLayer('esriworldimagery', show=False).add_to(m)

            # Add lines to the map
            add_lines(m)

            # Add stations to the map
            add_stations(m, station)
            
            html = ""
            if operator == "BA":
                # Test connections in popup
                # Get the station in the "bart_data" list with same station id as "station"
                old_station = next(old_station for old_station in old_bart_data if old_station["id"] == station["id"])
                html = f"<p>Connections: "
                for connection in old_station["connections"]:
                    html += f"""<span style="color: {colors["BA"][f'{connection}-N']}">{connection}</span>, """
                html += "</p>"

            # Add the GeoJSON layer
            # popup
            html = f"""<span style="background-color: {colors[operator][line]}; color: {"white" if line in ["CC", "ACETrain", "SMART"] else "black"}";>{line}</span>, """
            html = html[:-2]
            html += "</p>"

            p = folium.Popup(
                f"<p><b>Station</b>: {station['Name']}</p><br style='content: \" \";'><p><b>Line</b>: {html}</p><br style='content: \" \";'><p><b>Operator</b>: {op_to_name(operator)}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{operator}/{line}/{station['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
                max_width=265
            )
            folium.Marker(
                location=[station['Location']['Latitude'], station['Location']['Longitude']],
                popup=p,# f"<p>{station['Name']}</p><br><a href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{operator}/{line.replace(' ', '')}/{filename}'>View Station Map</a>",
                icon=makeBeautifyIcon(
                    icon=None,
                    border_color="#ff0000",
                    border_width=3,
                    text_color="#b3334f",
                    background_color="#a44fff",
                    icon_shape="circle",
                    inner_icon_style="opacity: 0; background-color: #a44fff",
                    icon_size=[16, 16],
                )
            ).add_to(m)

            # Add a 0.25 mile radius circle around the station
            folium.Circle(
                location=[station['Location']['Latitude'], station['Location']['Longitude']],
                radius=402.336,
                color='crimson',
                fill=False,
                tooltip="0.25 mile radius"
            ).add_to(m)

            # Add location
            # Add location control
            # Add drawings feature group
            drawings = folium.FeatureGroup(
                name="drawings"
            )
            drawings.add_to(m)
            m.add_child(LocateControl(strings={"title": "See you current location", "popup": "Your position"},))
            m.add_child(folium.LayerControl())
            Draw(
                feature_group=drawings, 
                export=True
            ).add_to(m)
            # Add measure control
            m.add_child(folium.plugins.MeasureControl())
            
            # Save the map
            print("Saving map to", filename)
            # path to folder: operator/line/station.html
            # Check if the folder exists
            if not os.path.exists(f"maps/point_25_mile/{operator}"):
                os.mkdir(f"maps/point_25_mile/{operator}")
            if not os.path.exists(f"maps/point_25_mile/{operator}/{line.replace(' ', '')}"):
                os.mkdir(f"maps/point_25_mile/{operator}/{line.replace(' ', '')}")

            m.save(f"maps/point_25_mile/{operator}/{line.replace(" ", "")}/{filename}")
            # break
        # break
    # break