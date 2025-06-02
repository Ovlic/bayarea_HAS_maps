
import folium, os, json, time
import transit_map
from muni_tracks3 import draw_tracks as actually_draw_tracks
from location_test import add_location_circles2 as add_location_circles
from utils import makeBeautifyIcon

# Function to time how long parts of the code take to run
# The decorator should have a parameter that customizes the output text and adds "{time} seconds" to the end of the output
# Example usage:
# @timeit("My cool function took ")
# def my_cool_function():
#    # Do something cool

def timeit(text="Function took ", end="\n", flush=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(f"{text}{end_time - start_time:.2f} s", end=end, flush=flush)
            return result
        return wrapper
    return decorator

# Test
# @timeit("Testing decorator took ")
# def test_function():
#     print("This is a test function.")
#     time.sleep(1)

# test_function()

# Fun custom color printing
RESET = '\033[0m'
BOLD = '\033[1m'
WHITE = '\033[37m'
to_rgb = lambda x: (x >> 16 & 255, x >> 8 & 255, x & 255)
str_to_hex = lambda x: hex(int(x, 16)) if "#" not in x else hex(int(x[1:], 16))
def get_color_escape(r, g, b, bold=False, background=False):
    return '\033[{};{};2;{};{};{}m'.format(1 if bold else 0, 38 if not background else 48, r, g, b)
    # return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def printf(text, color, bold=False, background=False, **kwargs):
    """
    Print text in a specific color with optional bold and background.
    :param color: Hex color code as a string (e.g., "#ff0000").
    :param text: Text to print.
    :param bold: Whether to print in bold.
    :param background: Whether to use the color as a background.
    """
    hex_color = str_to_hex(color)
    r, g, b = to_rgb(int(hex_color, 16))
    print(f"{get_color_escape(r, g, b, bold=bold, background=background)}{text}{RESET}", **kwargs)

# Hex: "#ed1c24", print Hello world with that color
# White
print(str_to_hex("#ed1c24"))
print(f"{get_color_escape(*to_rgb(0xffffff), bold=True)}Hello world{RESET}")
print(f"{get_color_escape(*to_rgb(0xaba682), bold=True)}Hello world{RESET}")



# Load colors
with open('data/colors.json', 'r') as f:
    colors = json.load(f)
# Load GeoJSON data for Caltrain
with open('data/lines/caltrain.geojson', 'r') as f:
        caltrain_geojson = json.load(f)
# Load GeoJSON data for SFO AirTrain
with open('data/track_data/sfo/blue_line.geojson', 'r') as f:
    sfo_blue_line_geojson = json.load(f)
with open('data/track_data/sfo/red_line.geojson', 'r') as f:
    sfo_red_line_geojson = json.load(f)
# Load GeoJSON data for VTA
with open('data/track_data/vta/orange_line.geojson', 'r') as f:
    vta_orange_line_geojson = json.load(f)
with open('data/track_data/vta/green_line.geojson', 'r') as f:
    vta_green_line_geojson = json.load(f)
with open('data/track_data/vta/blue_line.geojson', 'r') as f:
    vta_blue_line_geojson = json.load(f)
# Load GeoJSON data for ACE Train
with open('data/track_data/ace.geojson', 'r') as f:
    ace_geojson = json.load(f)
with open('data/train_bus/shapes.json', 'r') as f:
    shapes = json.load(f)
    # Get SMART coords
    smart_coords = shapes['SA']['t_5996501_b_84105_tn_0']
    # Get CC coords
    cc_coords = shapes['AM']['538']


def draw_tracks(m, op_in_names=False):
    caltrain_layer = folium.FeatureGroup(name="Caltrain")
    sfo_blue_line_layer = folium.FeatureGroup(name="SFO Blue Line")
    sfo_red_line_layer = folium.FeatureGroup(name="SFO Red Line")
    vta_orange_line_layer = folium.FeatureGroup(name="VTA Orange Line")
    vta_green_line_layer = folium.FeatureGroup(name="VTA Green Line")
    vta_blue_line_layer = folium.FeatureGroup(name="VTA Blue Line")
    ace_layer = folium.FeatureGroup(name="ACE")
    cc_layer = folium.FeatureGroup(name="CC")
    smart_layer = folium.FeatureGroup(name="SMART")


    def make_geojson(geojson, op, name, weight=4, tooltip=None, color=None, reverse_coords=False):
        if reverse_coords:
            # Reverse the coordinates in the GeoJSON
            for feature in geojson['features']:
                if 'geometry' in feature and feature['geometry']['type'] == 'LineString':
                    feature['geometry']['coordinates'] = [list(reversed(coord)) for coord in feature['geometry']['coordinates']]

        return folium.GeoJson(
            geojson,
            style_function=lambda feature: {
                'color': colors[op][name],
                'weight': weight,
            },
            tooltip=tooltip if tooltip else f"{transit_map.op_to_name(op)} {name}",
            name=tooltip if tooltip else f"{transit_map.op_to_name(op)} {name}",
            smooth_factor=0.1
        )
    
    def make_polyline(coords, op, name, weight=4, tooltip=None):
        return folium.PolyLine(
            coords, 
            color=colors[op][name],
            weight=weight,
            tooltip=tooltip if tooltip else f"{transit_map.op_to_name(op)} {name}",
            smooth_factor=0.1
        )
    
    # Draw SFO lines
    make_geojson(sfo_blue_line_geojson, 'SI', 'Blue Line AirTrain', tooltip="SFO Blue Line", weight=3, reverse_coords=True).add_to(sfo_blue_line_layer)
    make_geojson(sfo_red_line_geojson, 'SI', 'Red Line AirTrain', tooltip="SFO Red Line", weight=3, reverse_coords=True).add_to(sfo_red_line_layer)
    # Draw VTA Lines
    make_geojson(vta_orange_line_geojson, 'SC', 'Orange Line', tooltip="VTA Orange Line", weight=4, reverse_coords=True).add_to(vta_orange_line_layer)
    make_geojson(vta_green_line_geojson, 'SC', 'Green Line', tooltip="VTA Green Line", weight=4, reverse_coords=True).add_to(vta_green_line_layer)
    make_geojson(vta_blue_line_geojson, 'SC', 'Blue Line', tooltip="VTA Blue Line", weight=4, reverse_coords=True).add_to(vta_blue_line_layer)
    # Draw ACE Train
    make_geojson(ace_geojson, 'CE', 'ACETrain', tooltip="ACE Train", weight=5).add_to(ace_layer)
    # Draw CC
    make_polyline(cc_coords, 'AM', 'CC', tooltip="Capitol Corridor", weight=5).add_to(cc_layer)
    # Draw SMART
    make_polyline(smart_coords, 'SA', 'SMART', tooltip="SMART Train", weight=5).add_to(smart_layer)
    # Draw caltrain tracks
    folium.GeoJson(
        caltrain_geojson,
        style_function=lambda feature: {
            'color': '#FF0000',   # Red boundary line
            'weight': 5,          # Line thickness
        },
        tooltip="Caltrain",
        name="Caltrain",
        smooth_factor=0.1
    ).add_to(caltrain_layer)
    caltrain_layer.add_to(m)
    sfo_blue_line_layer.add_to(m)
    sfo_red_line_layer.add_to(m)
    vta_orange_line_layer.add_to(m)
    vta_green_line_layer.add_to(m)
    vta_blue_line_layer.add_to(m)
    ace_layer.add_to(m)
    cc_layer.add_to(m)
    smart_layer.add_to(m)
    # Draw BART and Muni tracks
    actually_draw_tracks(m, op_in_names=op_in_names)

def make_popup(stop):
    # Work on connections part of popup
    white_text_lines = ["L", "M", "N", "38R", "T", "Red", "Express", "Red Line", "CC", "ACETrain", "SMART"]
    white_or_black = lambda x: "white" if x in white_text_lines else "black"
    line_type = lambda x: "Bus" if x == "38R" else "Line"
    html = ""
    for connection in stop["connections"]:
        if connection in ["J", "K", "L", "M", "N", "T", "38R", "CA", "PH", "PM"]: the_op = "SF"
        elif connection in ["Blue", "Green", "Orange", "Yellow", "Red"]: the_op = "BA"
        elif connection in ["Orange Line", "Blue Line", "Green Line"]: the_op = "SC"
        elif connection in ["Red Line AirTrain", "Blue Line AirTrain"]: the_op = "SI"
        elif connection in ["Local Weekday", "Local Weekend", "Limited", "Express"]: the_op = "CT"
        elif connection in ["ACETrain"]: the_op = "CE"
        elif connection in ["CC"]: the_op = "AM"
        else:
            # No connections in file lines: SMART
            the_op = "SA"
        if the_op == "BA":
            connection_color = f"{connection}-N"
        else:
            connection_color = connection
        if the_op == "SF":
            connection_str = f"{connection} {line_type(connection)}"
        else:
            connection_str = connection

        html += f"""<span style="background-color: {colors[the_op][connection_color]}; color: {white_or_black(connection)}";>{connection_str}</span>, """
    html = html[:-2]
    p = folium.Popup(
        f"<p><b>Station</b>: {stop['Name']}</p><!--br style='content: \" \";'--><p><b>Coords</b>: {stop["Location"]["Latitude"]}, {stop["Location"]["Longitude"]}</p><!--br style='content: \" \";'--><p><b>Line{'s' if len(stop['connections'])>1 else ''}</b>: {html}</p><!--br style='content: \" \";'--><p><b>Operator</b>: {transit_map.op_to_name(stop['operator'])}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{stop['operator']}/{stop['connections'][0].replace(' ', '')}-N/{stop['id'].replace(' ', '_')}.html'><b>View Station Map</b></a>",
        max_width=265
    )
    return p



 # Load stations from file
with open('data/train_bus/stations.json', 'r') as f:
    raw_stations = json.loads(f.read())
    
with open('data/stations/stations_ace.json', 'r') as f:
    old_ace_data = json.load(f)

with open('data/stations/stations_cc.json', 'r') as f:
    old_cc_data = json.load(f)

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

with open('data/stations/stations_smart.json', 'r') as f:
    old_smart_data = json.load(f)

# Consolidate data into a single dictionary
stations = {}

# The if statement applies to all operators in the transit_map.operators list so this code is commented out
"""for op in transit_map.operators:
    if op in ['AM', 'CE', 'BA', 'SF', 'CT', 'SC', 'SI', 'SA']: continue
    __data = raw_stations[op]
    if op not in stations:
        stations[op] = {}
    for line, _data in __data.items():
        if line not in stations[op]:
            stations[op][line] = []
        for station in _data['Contents']['dataObjects']['ScheduledStopPoint']:
            station['operator'] = op
            stations[op][line].append(station)"""

# Add old data to the stations dictionary
for op, data in [('CE', old_ace_data), ('AM', old_cc_data), ('BA', old_bart_data), ('SF', old_muni_data), ('CT', old_ct_data), ('SC', old_vta_data), ('SI', old_sfo_data), ['SA', old_smart_data]]:
    if op not in stations:
        stations[op] = {}
    for station in data:
        if op == "CT":
            if "San Francisco Caltrain Station" in station['Name'] and "South " not in station['Name']:
                # Drop the southbound or northbound part of the name
                station['Name'] = "San Francisco Caltrain Station"
                # 37.776369,-122.3949635
                station['Location']['Latitude'] = "37.776369"
                station['Location']['Longitude'] = "-122.3949635"
                # print("Changing San Francisco Caltrain Station")
            if "22nd Street Caltrain Station" in station['Name']:
                # Drop the southbound or northbound part of the name
                station['Name'] = "22nd Street Caltrain Station"
                # 37.748, -122.392
                station['Location']['Latitude'] = "37.757583"
                station['Location']['Longitude'] = "-122.392404"
                # print("Changing 22nd Street Caltrain Station")
            if "Bayshore Caltrain Station" in station['Name']:
                # Drop the southbound or northbound part of the name
                station['Name'] = "Bayshore Caltrain Station"
                # 37.70766948153158, -122.40184374398838
                station['Location']['Latitude'] = "37.70766948153158"
                station['Location']['Longitude'] = "-122.40184374398838"
                # print("Changing Bayshore Caltrain Station")
        
        if 'connections' not in station:
            print(f"Station '{station['Name']}' has no connections!")

        for line in station['connections']:
            # Add the station to the appropriate operator and line
            if line not in stations[op]:
                stations[op][line] = []
            station_copy = station.copy()
            stations[op][line].append(station_copy)

save_progress = True
save_file = "updated_stations.py"
save_content = "stations = [\n"
width = os.get_terminal_size().columns 

# Loop through stations to create a map for each one
loops = 2
try:
    for op, lines in stations.items():
        print(f"Operator: '{op}'\n")
        for line, stops in lines.items():
            # Get the line color
            line_color = str_to_hex(colors[op].get(line, "#ffffff"))  # Default to white if not found
            print(f"\tLine: '", end="", flush=True)
            printf(f"{line}", line_color, bold=True, end="'\n", flush=True)

            for stop in stops:
                printf(f"\t\tStop: ", color=line_color, end="", flush=True)
                printf(f"'{stop['Name']}'", "#ffffff", bold=True, flush=True)

                filename = f"{stop['id'].replace(' ', '_')}.html"

                @timeit("Done. (", end=")\n")
                def make_folium_map_wrapper():
                    print(f"\t\tCreating map for '{stop['Name']}'... ", end='', flush=True)

                    # Create a folium map centered on the station
                    m = folium.Map(
                        location=[stop['Location']['Latitude'], stop['Location']['Longitude']], 
                        zoom_start=15,
                        tiles='cartodbpositron',
                        prefer_canvas=True,
                    )
                    # Add tiles to the map
                    transit_map.add_tiles(m)
                    # Add lines to the map
                    draw_tracks(m, op_in_names=True)

                    # Add the stations to the map (Exclude the current stop from being included)
                    circle_shapes = transit_map.add_stations(m, shaded_area=True, test=True, ignored_stops=stop['Name'])
                    # Add the specific station
                    station_marker = folium.Marker(
                        location=[stop['Location']['Latitude'], stop['Location']['Longitude']],
                        popup=make_popup(stop),
                        icon=makeBeautifyIcon(
                            icon=None,
                            border_color="#ff0000",
                            border_width=3,
                            text_color="#b3334f",
                            background_color="#a44fff",
                            icon_shape="circle",
                            inner_icon_style="opacity: 0; background-color: #a44fff",
                            icon_size=[16, 16],
                        ),
                        zIndexOffset=1000,  # Keep the marker on top
                    ).add_to(m)

                    # Add a 0.25 mile circle around the station
                    # Add a 0.25 mile radius circle around the station
                    station_circle = folium.Circle(
                        location=[stop['Location']['Latitude'], stop['Location']['Longitude']],
                        radius=402.336,
                        color='crimson',
                        fill=False,
                        tooltip="0.25 mile radius"
                    ).add_to(m)

                    # Keep on top
                    m.keep_in_front(station_circle)
                    # Add plugins to the map
                    transit_map.add_plugins(m)

                    # Add location circles
                    add_location_circles(m, [402.336, 804.672, 1609.34, 4828.03, 8046.72, 11265.4], ["Radius: 0.25 miles", "Radius: 0.5 miles", "Radius: 1 mile", "Radius: 3 miles", "Radius: 5 miles", "Radius: 7 miles"])
                    return m

                m = make_folium_map_wrapper()

                # Save the map to a file
                # path to folder: operator/line/station.html
                # Check if the folder exists
                if not os.path.exists(f"maps/point_25_mile/{op}"):
                    os.mkdir(f"maps/point_25_mile/{op}")
                if not os.path.exists(f"maps/point_25_mile/{op}/{line.replace(' ', '')}"):
                    os.mkdir(f"maps/point_25_mile/{op}/{line.replace(' ', '')}")

                filepath = f"maps/point_25_mile/{op}/{line.replace(' ', '')}/{filename}"

                @timeit("Done. (", end=")\n")
                def save_map(m, fp):
                    # print("\t\tSaving map took ...", end=' ', flush=True)
                    print(f"\t\tSaving map for '{stop['Name']}' at '{filepath}'... ", end='', flush=True)
                    m.save(fp)
                
                @timeit("Done. (", end=")\n")
                def add_favicons(m, fn):
                    print(f"\t\tAdding favicons ... ", end='', flush=True)
                    transit_map.add_favicons(filename=fn)

                
                # m.save(filepath)
                save_map(m, filepath)
                # transit_map.add_favicons(filename=filepath)
                add_favicons(m, filepath)
                # print(f"\t\tSaved map for '{stop['Name']}' at '{filepath}'")
                # Add the station to the save content
                if save_progress:
                    # save_content += f"    {{\n        'id': '{stop['id']}',\n        'Name': '{stop['Name']}',\n        'Location': {{'Latitude': {stop['Location']['Latitude']}, 'Longitude': {stop['Location']['Longitude']}}},\n        'connections': {stop['connections']},\n        'operator': '{stop['operator']}'\n    }},\n"
                    save_content += f"""    {{'id': '{stop['id']}',\n        'Name': '{stop['Name']}',\n        'Location': {{'Latitude': {stop['Location']['Latitude']}, 'Longitude': {stop['Location']['Longitude']}}},\n        'connections': {stop['connections']},\n        'operator': '{stop['operator']}'\n    }},\n"""

                loops -= 1
                if loops <= 0: # Stop after 2 loops for testing purposes
                    print("Breaking after 2 loops for testing purposes.")
                    break

                # Station break
                print()

            # Line break
            print('-' * width)
            break
        # Operator break
        print('=' * width)
        break
finally: # This block will always run, even if an error occurs, plus after the station data is saved the error is still raised
    print("Stop processing stations, saving progress if enabled...")
    if save_progress:
        save_content += "]\n"
        with open(save_file, "w") as f:
            f.write(save_content)
        print(f"Saved stations to '{save_file}'")
    else:
        print("Save progress is disabled. Not saving stations.")
