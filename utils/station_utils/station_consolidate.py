
import json

with open('train_bus/stations.json', 'r') as f:
    data = json.load(f)

old_bart_data = []
old_muni_data = []
old_ct_data = []
old_vta_data = []
old_sfo_data = []

for line_id in data["BA"]:
    if "-S" in line_id: continue
    for station in data['BA'][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
        # is station already in old_bart_data?
        if any(station["id"] == old_station["id"] for old_station in old_bart_data):
            # get old station
            old_station = next(old_station for old_station in old_bart_data if old_station["id"] == station["id"])
            # add line_id to connections (without -N or -S)
            old_station["connections"].append(line_id[:-2])
            # old_station['operator'] = 'BA'
            continue
        
        # check if connections key exists
        if "connections" not in station:
            station["connections"] = []
        # add line_id to connections (without -N or -S)
        station["connections"].append(line_id[:-2])
        station['operator'] = 'BA'
        old_bart_data.append(station)

# Do muni
for line_id in data["SF"]:
    print(line_id)
    for station in data['SF'][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
        # is station already in old_bart_data?
        if any(station["id"] == old_station["id"] for old_station in old_muni_data):
            # get old station
            old_station = next(old_station for old_station in old_muni_data if old_station["id"] == station["id"])
            old_station["connections"].append(line_id)
            # old_station['operator'] = 'SF'
            continue
        
        # check if connections key exists
        if "connections" not in station:
            station["connections"] = []
        # add line_id to connections (without -N or -S)
        station["connections"].append(line_id)
        station['operator'] = 'SF'
        old_muni_data.append(station)

for line_id in data["CT"]:
    print(line_id)
    for station in data['CT'][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
        # is station already in old_bart_data?
        if any(station["id"] == old_station["id"] for old_station in old_ct_data):
            # get old station
            old_station = next(old_station for old_station in old_ct_data if old_station["id"] == station["id"])
            old_station["connections"].append(line_id)
            # old_station['operator'] = 'CT'
            continue
        
        # check if connections key exists
        if "connections" not in station:
            station["connections"] = []
        # add line_id to connections (without -N or -S)
        station["connections"].append(line_id)
        station['operator'] = 'CT'
        old_ct_data.append(station)
        
for line_id in data['SC']:
    print(line_id)
    for station in data['SC'][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
        if any(station["id"] == old_station["id"] for old_station in old_vta_data):
            old_station = next(old_station for old_station in old_vta_data if old_station["id"] == station["id"])
            old_station["connections"].append(line_id)
            # old_station['operator'] = 'SC'
            continue
        if "connections" not in station:
            station["connections"] = []
        station["connections"].append(line_id)
        station['operator'] = 'SC'
        old_vta_data.append(station)


for line_id in data['SI']:
    print(line_id)
    for station in data['SI'][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]:
        if any(station["id"] == old_station["id"] for old_station in old_sfo_data):
            old_station = next(old_station for old_station in old_sfo_data if old_station["id"] == station["id"])
            old_station["connections"].append(line_id)
            # old_station['operator'] = 'SI'
            continue
        if "connections" not in station:
            station["connections"] = []
        station["connections"].append(line_id)
        station['operator'] = 'SI'
        old_sfo_data.append(station)



# Get the station in the list with id EMBR
emb = next(station for station in old_muni_data if station["id"] == "16992")
print(emb)

with open("stations_bart.json", "w") as f:
    json.dump(old_bart_data, f, indent=4)

with open("stations_muni.json", "w") as f:
    json.dump(old_muni_data, f, indent=4)

with open("stations_ct.json", "w") as f:
    json.dump(old_ct_data, f, indent=4)

with open("stations_vta.json", "w") as f:
    json.dump(old_vta_data, f, indent=4)

with open("stations_sfo.json", "w") as f:
    json.dump(old_sfo_data, f, indent=4)