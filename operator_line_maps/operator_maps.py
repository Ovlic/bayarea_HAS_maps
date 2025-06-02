

import json, folium
from operator_line_maps.classes import Station, Line

# Load data from "data/ops.json"
with open("data/ops.json", "r") as f:
    data = json.load(f)

new_data = {}
# Convert lines to Line objects
# Convert stations to Station objects

# Form of data:
# {
#     "operator": {
#         "line": {
#             "lines": [line1, line2, ...],
#             "stations": [station1, station2, ...]
#         },
#         ...
#     },
#     ...
# }

for op, lines in data.items():
    new_data[op] = {}
    for line_name, more_data in lines.items():
        if line_name == "ACE": line_name = "ACETrain"
        # Rename "lines" to "layers" (only in the code) since there is already a lines key
        layers = more_data['line']
        stations = more_data['stations']
        if layers == []:
            print("No layers")
            continue
        # print(line_name+": ", end="")
        # print(stations)
        new_data[op][line_name] = {
            "lines": [Line.from_feature(layer, op, line_name) for layer in layers],
            "stations": [Station.from_feature(s, op, line_name) for s in stations]
        }
        # if op == "AM":
            # print(f"Stations for amtrack: {len(new_data[op][line_name]['stations'])}")
        # for layer in layers:
        #     print(lines)
            
        
        # stations = more_data['stations']
        # for station in stations:
        #     print(station)
        #     # Stations
        #     new_data[op][line_name]['stations'] = [Station(s, op, line_name) for s in stations]

for op, lines in new_data.items():
    # Loop through the stations and find the midpoint of all the stations, that will be the center of the map
    station_coords = []
    for line_name, data in lines.items():
        for station in data['stations']:
            station_coords.append((station.lat, station.lon))


    # Extract min/max latitudes and longitudes
    min_lat = min(lat for lat, lon in station_coords)
    max_lat = max(lat for lat, lon in station_coords)
    min_lon = min(lon for lat, lon in station_coords)
    max_lon = max(lon for lat, lon in station_coords)

    # Create a folium map centered at the average location
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    op_m = folium.Map(
        location=[center_lat, center_lon], 
        zoom_start=10, 
        tiles="cartodbpositron"
    )
    op_m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

    fgs = {}

    # Add lines
    for line_name, data in lines.items():
        if op not in fgs:
            fgs[op] = {}
        if line_name not in fgs[op]:
            fgs[op][line_name] = folium.FeatureGroup(name=f"{op} {line_name}")
        the_fg = fgs[op][line_name]
        for line in data['lines']:
            # Draw polyline
            # print(f"Op: {line.operator}; Line: {line.line_id}; Color: {line.color}")
            the_fg.add_child(line.to_polyline())
        # m.add_child(the_fg)

# Add stations
# for op, lines in new_data.items():
    for line_name, data in lines.items():
        the_fg = fgs[op][line_name]
        for station in data['stations']:
            the_fg.add_child(station.to_marker())
        op_m.add_child(the_fg)

    # Add feature groups
    for op, lines in fgs.items():
        for line_name, fg in lines.items():
            op_m.add_child(fg)

    # Add layer control
    folium.LayerControl().add_to(op_m)

    # Save map
    op_filename = f"local/op/{op}.html"
    op_m.save(op_filename)
    
