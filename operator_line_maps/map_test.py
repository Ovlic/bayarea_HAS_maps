

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

# Create a map
m = folium.Map(location=[37.7749, -122.4194], zoom_start=10, tiles="cartodbpositron")

fgs = {}

# Add lines
for op, lines in new_data.items():
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
for op, lines in new_data.items():
    for line_name, data in lines.items():
        the_fg = fgs[op][line_name]
        # the_fg = folium.FeatureGroup(name=f"{op} {line_name} Stations")
        for station in data['stations']:
            # print("Station")
            # print(station.stop)
            # Draw station
            # Print operator, line, and station name
            # print(f"Op:{op} Line: {line_name} Station: {station.name}")
            the_fg.add_child(station.to_marker())
        m.add_child(the_fg)

# Add feature groups
for op, lines in fgs.items():
    for line_name, fg in lines.items():
        m.add_child(fg)

# Add layer control
folium.LayerControl().add_to(m)

# Save map
m.save("local/map_test.html")
        