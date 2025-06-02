
# Very similar to station_map_generator.py, but for lines instead of stations, and without a circle around the location

import folium, json
from pprint import pprint

from utils import get_operator
import transit_map
from operator_line_maps.classes import Station, Line
from location_test import (
    add_location_circle2 as add_location_circle,
    add_location_circles2 as add_location_circles,
)
from folium.plugins import LocateControl
from folium import Element
from folium.map import Layer

from json import JSONEncoder

# https://stackoverflow.com/a/38764817
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default



# Load data from files
with open('data/colors.json', 'r') as f:
    colors = json.loads(f.read())

# Order of maps directory:
# Folder: operator_name
#     index.html -> Map of all lines for that operator
#     Folder: line_name
#         index.html -> Map of that line
#         html files for each station

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

with open("data/stations/stations_ace.json", "r") as f:
    old_ace_data = json.load(f)

with open("data/stations/stations_cc.json", "r") as f:
    old_cc_data = json.load(f)

with open("data/stations/stations_smart.json", "r") as f:
    old_smart_data = json.load(f)


# Load lines from file
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

muni_lines = {'F': muni_f_geojson, 'J': muni_j_geojson, 'K': muni_k_geojson, 'L': muni_l_geojson, 'M': muni_m_geojson, 'N': muni_n_geojson, 'T': muni_t_geojson, '038R': muni_38R_geojson, 'CA': california_cable_car_geojson, 'PH': powell_hyde_cable_car_geojson, 'PM': powell_mason_cable_car_geojson, '38R': muni_38R_geojson}

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

# Make a dictionary of all operators that holds a dictionary of all lines for that operator that holds both the line data and the station data
ops = {}
added_stations = {} # Dictionary with the operators as keys, then each line, with station names in an array

for operator in transit_map.operators:
    if operator not in ops:
        ops[operator] = {}
    
    """# Add stations
    for line_id in stations[operator]:
        if operator in ['BA', 'SF', 'CT', 'SC', 'SI']: continue
        for stop in stations[operator][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
            the_station = Station(stop, line_id, operator)
            if line_id not in ops[operator]:
                ops[operator][line_id] = {}
            if 'stations' not in ops[operator][line_id]:
                ops[operator][line_id]['stations'] = []
            ops[operator][line_id]['stations'].append(the_station)
    """
    # Add lines
    if operator in ["BA", "SF", "CE"]: continue
    if operator not in shapes:
        continue

    for line_id in shapes[operator]:
        # Find the route trip ID for the line
        rti = None
        for route in route_trip_ids[operator]:
            # Check for empty list
            if route_trip_ids[operator][route]['trip_ids'] != []:
                if route_trip_ids[operator][route]['trip_ids'][0] == line_id:
                    rti = route
                    break
        
        # TESTING!!!
        print(f"RTI: {rti}")
        if rti in ['Limited', 'Express', 'Local Weekday', 'Local Weekend']:
            # print(f"Skipping Caltrain, testing new way of drawing lines")
            continue
        if rti in ["5R", "9R", "14R", "28R"]: continue
        coords = []
        for pos in shapes[operator][line_id]:
            # print(pos)
            if pos[0] > pos[1]:
                coords.append([pos[0], pos[1]])
            else:
                coords.append([pos[1], pos[0]])

        if line_id == "805":
            print(f"Line 805 for {operator}")
            # line_id = rti
            adjusted_line_id = rti
            print(shapes['CT']["805"])
            print("------")
            print(coords)
        elif line_id == "538":
            print(f"Line 538 for {operator}")
            # line_id = rti
            adjusted_line_id = rti
            # print(shapes['AM']["538"])
            # print("------")
            # print(coords)
        elif line_id == "708":
            print(f"Line 708 for {operator}")
            # line_id = rti
            adjusted_line_id = rti
            # print(shapes['AM']["708"])
            # print("------")
            # print(coords)
        elif line_id == "1068":
            print(f"Line 1068 for {operator}")
            # line_id = rti
            adjusted_line_id = rti
            # print(shapes['AM']["1068"])
            # print("------")
            # print(coords)
        elif line_id in ["3732228", "3732540", "3731939", "t_5996501_b_84105_tn_0"]:
            print(f"Line {line_id} for {operator}")
            adjusted_line_id = rti
        else:
            adjusted_line_id = line_id
        # coords = shapes[operator][line_id]
        the_line = Line(coords, operator, adjusted_line_id)
        if adjusted_line_id not in ops[operator]:
            ops[operator][adjusted_line_id] = {}
        if 'line' not in ops[operator][adjusted_line_id]:
            ops[operator][adjusted_line_id]['line'] = []
        if 'stations' not in ops[operator][adjusted_line_id]:
            ops[operator][adjusted_line_id]['stations'] = []
        print(f"Adding line {adjusted_line_id} for {operator}")
        ops[operator][adjusted_line_id]['line'].append(the_line)
# """
    
# BART
for name, line in bart_lines.items():
    if "BA" not in ops:
        # print("BA not in ops")
        ops['BA'] = {}
    else:
        # print(ops['BA'])
        pass
    if name not in ops['BA']:
        ops['BA'][name] = {}
    ops['BA'][name]['line'] = [Line.from_feature(l, 'BA', name) for l in line['features']]
    ops['BA'][name]['stations'] = []


def add_connections(stop):
    # Regenerate connections
    new_connections = {}
    if 'connections' not in stop:
        print(f"Stop {stop['Name']} has no connections")
        print(stop)
    for connection in stop['connections']:
        if connection == "FBUS": # Bus replacement service
            continue
        the_op = get_operator(connection)
        if the_op not in new_connections:
            new_connections[the_op] = []
        new_connections[the_op].append(connection)
    stop['connections'] = new_connections

    # print(stop['connections'])
    for the_op, connections in stop['connections'].items():
        if the_op not in added_stations:
            added_stations[the_op] = {}
        for c_name in connections:
            # Check if added_stations has the keys and data
            if c_name not in added_stations[the_op]:
                added_stations[the_op][c_name] = []
            if c_name not in ops[the_op]:
                ops[the_op][c_name] = {"line": [], "stations": []}
            # Check if the station is already added for that line
            if stop['Name'] in added_stations[the_op][c_name]:
                print(f"Station {stop['Name']} already added for {c_name} in {the_op}")
                continue
            added_stations[the_op][c_name].append(stop['Name'])
            the_station = Station(stop, c_name, the_op)
            # print(c_name)
            ops[the_op][c_name]['stations'].append(the_station)


# Add stations
for stop in old_bart_data:
    # Check if stop name is in transit_map.bart_muni_stations
    # duplicate = False
    for id, station_data in transit_map.bart_muni_stations.items():
        for other_name in station_data['other_names']:
            if stop['Name'] == other_name:
                ## Skip this station (it's a duplicate)
                # print(f"Skipping duplicate station {stop['Name']}")
                # duplicate = True
                # Change the name of the station
                stop['Name'] = other_name
                break
    # if duplicate:
        # continue
    # print(f"Stop id: {stop['id']}")
    add_connections(stop)


        # if c_name in ["J", "K", "L", "M", "N"]: # MUNI
        #     continue # Dont add muni to bart!
        # # Get operator of c_name
        # the_station = Station(stop, c_name, 'BA')
        # print(f"Station: {the_station.name}; Line: {c_name}")
        # ops['BA'][c_name]['stations'].append(the_station)

# Muni
for name, line in muni_lines.items():
    if name == "038R": continue # duplicate of "38R"
    if name not in ops['SF']:
        ops['SF'][name] = {}
    ops['SF'][name]['line'] = [Line.from_feature(l, 'SF', name) for l in line['features']]
    if 'stations' not in ops['SF'][name]:
        print(f"Adding stations for {name}")
        ops['SF'][name]['stations'] = []

# Add stations
for stop in old_muni_data:
    if stop['Name'] in transit_map.ignored_stops:
        continue
    # Check if stop name is in transit_map.bart_muni_stations
    duplicate = False
    for id, station_data in transit_map.bart_muni_stations.items():
        for other_name in station_data['other_names']:
            if stop['Name'] == other_name:
                # Skip this station (it's a duplicate)
                # print(f"Skipping duplicate station {stop['Name']}")
                # duplicate = True
                # break
                # Change the name of the station
                stop['Name'] = station_data['name']
    
    for name, station_data in transit_map.combine_stations.items():
        for other_name in station_data['other_names']:
            if other_name in added_stations:
                duplicate = True
                break
    if duplicate:
        continue
    # print(f"Stop id: {stop['id']}")
    add_connections(stop)
    # the_station = Station(stop, name, 'SF')
    # for c_name in the_station.connections:
    #     if c_name in ["Red", "Orange", "Yellow", "Green", "Blue"]: # BART
    #         continue # Dont add bart to muni!
    #     if c_name == "FBUS": # Bus replacement service
    #         continue
    #     ops['SF'][c_name]['stations'].append(the_station)


# Caltrain
# ops['CT']['Caltrain'] = {}
# ops['CT']['Caltrain']['line'] = [Line.from_feature(l, 'CT', 'Caltrain') for l in caltrain_geojson['features']]
# ops['CT']['Caltrain']['stations'] = []
# # Add stations
# for stop in old_ct_data:
#     the_station = Station(stop, 'Caltrain', 'CT')
#     ops['CT']['Caltrain']['stations'].append(the_station)
for name in ['Limited', 'Express', 'Local Weekday', 'Local Weekend']: # South County is already added previously
    ops['CT'][name] = {}
    ops['CT'][name]['line'] = [Line.from_feature(l, 'CT', name) for l in caltrain_geojson['features']]
    ops['CT'][name]['stations'] = []
# Add south county
# ops['CT']['South County'] = {"line": [], "stations": []}

# Add stations
for stop in old_ct_data:
    # print(f"Stop id: {stop['id']}")
    # print("Add caltrain stations")
    add_connections(stop)

# ACE
ops['CE']['ACETrain'] = {}
ops['CE']['ACETrain']['line'] = [Line.from_feature(l, 'CE', 'ACETrain') for l in ace_geojson['features']]
ops['CE']['ACETrain']['stations'] = []

# Add stations
for stop in old_ace_data:
    if "connections" not in stop:
        stop['connections'] = ["ACETrain"]
    if 'id' not in stop:
        # print("Stop has no id")
        # print(stop)
        raise Exception("Stop has no id")
    # print(f"ACE Stop id: {stop['id']}")
    add_connections(stop)

# VTA
# Add stations
for stop in old_vta_data:
    # print(f"Stop id: {stop['id']}")
    add_connections(stop)

# SFO
# Add stations
for stop in old_sfo_data:
    # print(f"Stop id: {stop['id']}")
    add_connections(stop)

# CC
# ACE
# ops['AM']['CC'] = {}
ops['AM']['CC']['stations'] = []

# Add stations
for stop in old_cc_data:
    if "connections" not in stop:
        stop['connections'] = ["CC"]
    if 'id' not in stop:
        # print("Stop has no id")
        # print(stop)
        raise Exception("Stop has no id")
    # print(f"ACE Stop id: {stop['id']}")
    add_connections(stop)

# SMART
ops['SA']['SMART']['stations'] = []
# Add stations
for stop in old_smart_data:
    if "connections" not in stop:
        stop['connections'] = ["SMART"]
    add_connections(stop)


# Test by dumping the data to a file
with open("data/ops.json", "w") as f:
    f.write(json.dumps(ops, indent=4))