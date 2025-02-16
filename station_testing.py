
from my_session import MySession
import json, time, os, dotenv
from requests.exceptions import HTTPError

dotenv.load_dotenv()

key = os.getenv('API_511')
session = MySession(key)
load_from_file = True
load_trip_ids = True

operators = ['CE', 'BA', 'CT', 'AM', 'SI', 'SF', 'SA', 'SC'] # SI maybe, its for the airport


def get_stations(op, line_id):
    # Get the stations
    url = f"https://api.511.org/transit/stops?operator_id={op}&line_id={line_id}"

    response = session.get(url)
    # print(response.text)

    # with open('stations.txt', 'w') as f:
    #     f.write(response.text)
    out = json.loads(response.text.encode().decode('utf-8-sig'))

    return out

def get_lines(op):
    # Test with lines
    url = f"https://api.511.org/transit/lines?operator_id={op}"

    response = session.get(url)
    # print(response.text)
    out = json.loads(response.text.encode().decode('utf-8-sig'))

    # with open('lines.txt', 'w') as f:
    #     # Convert to pretty json with a tab as an indent (not possible??)
    #     f.write(json.dumps(out, indent=4))

    return out

def get_shapes(op, trip_id):
    # Get the shapes
    url = f"https://api.511.org/transit/shapes?operator_id={op}&trip_id={trip_id}"
    response = session.get(url)
    out = json.loads(response.text.encode().decode('utf-8-sig'))

    return out

def extract_shapes(data):
    www = data['Content']['TimetableFrame']['vehicleJourneys']['ServiceJourney']['LinkSequenceProjection']['LineString']['pos'] # What we want
    l1_coords = []
    for ll in www:
        # Split by space (coords are in this format: "lat, lon")
        lat, lon = ll.split(" ")
        l1_coords.append((float(lat), float(lon)))

    return l1_coords

def get_timetable(op, line_id):
    url = f"https://api.511.org/transit/timetable?operator_id={op}&line_id={line_id}"
    response = session.get(url)
    out = json.loads(response.text.encode().decode('utf-8-sig'))

    return out



# exit(get_shapes("CE"))


# # Start with SC
# op = 'CT'

# # The lines we want to use have 'TransportMode' == 'metro' or 'rail'
# get_lines(op)
if not load_from_file:
    lines = {}
    for op in operators:
        print(op, end="... ")
        lines[op] = get_lines(op)
        time.sleep(1.5)
    print("Done\nSaving to file...")
    with open('lines.json', 'w') as f:
        f.write(json.dumps(lines, indent=4))
    print("Done")

    # Loop through and get the lines with 'TransportMode' == 'metro' or 'rail' or 'cableway'
    print("Getting rail lines...")
    rail_lines = {}
    for op in operators:
        for line in lines[op]:
            if line['TransportMode'] in ['metro', 'rail', 'cableway']:
                if op not in rail_lines:
                    rail_lines[op] = []
                rail_lines[op].append(line)
                print(line)

    print("Done\nSaving to file...")
    with open('rail_lines.json', 'w') as f:
        f.write(json.dumps(rail_lines, indent=4))
    print("Done")

    # Get stations of all rail lines
    print("Getting stations...")
    stations = {}
    for op in rail_lines:
        for line in rail_lines[op]:
            print(f"Getting stations for {line['Id']}...", end=" ")
            if op not in stations:
                stations[op] = {}
            stations[op][line['Id']] = get_stations(op, line['Id'])
            print("Done")
            time.sleep(1.5)

    print("Done\nSaving to file...")
    with open('stations.json', 'w') as f:
        f.write(json.dumps(stations, indent=4))
    print("Done")

else:
    print("Loading from file...")
    # Load lines from lines.json
    with open('lines.json', 'r') as f:
        lines = json.load(f)

    # Load rail lines from rail_lines.json
    with open('rail_lines.json', 'r') as f:
        rail_lines = json.load(f)

    # Load stations from stations.json
    with open('stations.json', 'r') as f:
        stations = json.load(f)
    


# exit(get_timetable("CT", "Limited"))
# ['Content']['TimetableFrame'][num]['vehicleJourneys']['ServiceJourney']['id']

# Get shapes of all rail lines
# Start with getting trip_ids
if not load_trip_ids:
    print("Getting trip_ids...")
    trip_ids = {}
    route_trip_ids = {}
    for op in rail_lines:
        if op not in route_trip_ids:
            route_trip_ids[op] = {}
        for line in rail_lines[op]:
            print(f"Getting trip_ids for {line['Id']}...", end=" ")
            if op not in trip_ids:
                trip_ids[op] = []
            if line['Id'] not in route_trip_ids[op]:
                route_trip_ids[op][line['Id']] = {"trip_ids": []}
            try:
                sj = get_timetable(op, line['Id'])['Content']['TimetableFrame'][0]['vehicleJourneys']['ServiceJourney']
                # Count the amount of calls (we want the one with the most calls)
                max_calls = 0
                max_calls_i = 0
                for i in range(len(sj)):
                    # Get number of calls
                    calls = 0
                    for call in sj[i]['calls']['Call']:
                        calls += 1
                    
                    if calls > max_calls:
                        max_calls = calls
                        max_calls_i = i

                trip_ids[op].append(sj[max_calls_i]['id'])
                route_trip_ids[op][line['Id']]['trip_ids'].append(sj[max_calls_i]['id'])
                #trip_ids[op].append(sj['id'])
                print("Done")
            except Exception as e:
                print(type(e), end=": ")
                print(e)
                # print type of exception
                if type(e) == HTTPError:
                    continue
                print(get_timetable(op, line['Id']))
                raise e
                
            time.sleep(1.5)

    print("Done\nSaving to file...")
    with open('trip_ids.json', 'w') as f:
        f.write(json.dumps(trip_ids, indent=4))
    print("Done")

    with open('route_trip_ids.json', 'w') as f:
        f.write(json.dumps(route_trip_ids, indent=4))
    print("Done")
else:
    print("Loading from file...")
    with open('trip_ids.json', 'r') as f:
        trip_ids = json.load(f)

    with open('route_trip_ids.json', 'r') as f:
        route_trip_ids = json.load(f)

# Load colors
with open('colors.json', 'r') as f:
    colors = json.load(f)
# Get shapes
print("Getting shapes...")
shapes = {}
for op in trip_ids:
    for trip_id in trip_ids[op]:
        print(f"Getting shapes for {trip_id}...")
        if op not in shapes:
            shapes[op] = {}
        # Identify which line the trip_id belongs to and save it to the line variable
        line = None
        for line_id in route_trip_ids[op]:
            if trip_id in route_trip_ids[op][line_id]['trip_ids']:
                line = line_id
                break
        shapes[op][trip_id] = get_shapes(op, trip_id)
        # Add the shape to route_trip_ids
        route_trip_ids[op][line]['shape'] = shapes[op][trip_id]
        time.sleep(1.5)

# Shorten the shapes
print("Shortening shapes...")
for op in shapes:
    for line_id in shapes[op]:
        shapes[op][line_id] = extract_shapes(shapes[op][line_id])
        
for op in route_trip_ids:
    for line_id in route_trip_ids[op]:
        if 'shape' in route_trip_ids[op][line_id]:
            route_trip_ids[op][line_id]['shape'] = extract_shapes(route_trip_ids[op][line_id]['shape'])
        # Add the color
        route_trip_ids[op][line_id]['color'] = colors[op][line_id]


print("Done\nSaving to file...")
with open('shapes.json', 'w') as f:
    f.write(json.dumps(shapes, indent=4))
print("Done")

with open('route_trip_ids.json', 'w') as f:
    f.write(json.dumps(route_trip_ids, indent=4)
)
