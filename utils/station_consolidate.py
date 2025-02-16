
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
        ]
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
        ]
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
        ]
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
        ]
    },
    "BALB": {
        "lines": [
            "Red-N",
            "Yellow-N",
            "Green-N",
            "Blue-N",
            "J",
            "K",
        ], # Metro Balboa Park Station/Outbound, Metro Balboa Park Station/Downtown == BALB
        "other_names": [
            "Balboa Park BART/Mezzanine Level",
        ]
    },
}

caltrain_other_stations = {
    "70261": { # San Jose Diridon Caltrain Station
        "lines": [
            "Local Weekday",
            "Local Weekend",
            "Limited",
            "Express",
            # ACE
            "ACETrain",
            # CC
            "CC",
            # VTA
            "Green Line"
        ],
        "other_names": [
            "San Jose Diridon Caltrain Station",
            "San Jose",
            "Diridon Station",
            "San Jose Station"
        ]
    },
    "70241": { # Santa Clara Caltrain Station
        "lines": [
            "Local Weekday",
            "Local Weekend",
            "Limited",
            # ACE
            "ACETrain",
            # CC
            "CC"
        ],
        "other_names": [
            "Santa Clara Caltrain Station",
            "Santa Clara  Station",
            "University-Santa Clara"
        ]
    },
    "70211": { # Mountain View Caltrain Station
        "lines": [
            "Local Weekday",
            "Local Weekend",
            "Limited",
            "Express",
            # VTA
            "Orange Line",
        ],
        "other_names": [
            "Mountain View Caltrain Station",
            "Mountain View Station"
        ]
    },
    "70061": { # Millbrae Caltrain Station
        "lines": [
            "Local Weekday",
            "Local Weekend",
            "Limited",
            "Express",
            # BART
            "Red",
            "Yellow"
        ],
        "other_names": [
            "Millbrae Caltrain Station",
            "Millbrae (Caltrain Transfer Platform)"
        ]
    }
}

if __name__ == "__main__":
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
            # Check if station is one of the bart stations (in the "other_names" list for every station)
            for bart_station, value in bart_muni_stations.items():
                if station["Name"] in value["other_names"]:
                    # print(f"Found {station['Name']} in bart_muni_stations")
                    # print(bart_station)
                    # print(value)
                    # get the bart station
                    found = False
                    for old_station in old_bart_data:
                        if old_station["id"] == bart_station:
                            bart_station = old_station
                            found = True
                            break
                    assert found, f"Could not find {bart_station} in old_bart_data"

                    # add line_id to connections
                    # Check if line_id is already in connections
                    if line_id in bart_station["connections"]:
                        # print(f"Line {line_id} already in connections")
                        break
                    bart_station["connections"].append(line_id)
                    # bart_station['operator'] = 'SF'
                    break
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
            for caltrain_station, value in caltrain_other_stations.items():
                if station["Name"] in value["other_names"]:
                    # Add the connections
                    station["connections"] = value["lines"]
            #         print(f"Found {station['Name']} in caltrain_other_stations")
            #         print(caltrain_station)
            #         print(value)
            #         # get the caltrain station
            #         found = False
            #         for old_station in old_ct_data:
            #             if old_station["id"] == caltrain_station:
            #                 caltrain_station = old_station
            #                 found = True
            #                 break
            #         assert found, f"Could not find {caltrain_station} in old_ct_data"

            #         # add line_id to connections
            #         # Check if line_id is already in connections
            #         if line_id in caltrain_station["connections"]:
            #             print(f"Line {line_id} already in connections")
            #             break
            #         caltrain_station["connections"].append(line_id)
            #         # caltrain_station['operator'] = 'CT'
            #         break

            # is station already in old_bart_data?
            if any(station["id"] == old_station["id"] for old_station in old_ct_data):
                # get old station
                old_station = next(old_station for old_station in old_ct_data if old_station["id"] == station["id"])
                if line_id in old_station["connections"]:
                    # print(f"Line {line_id} already in connections")
                    continue
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
            # Check if station is one of the caltrain stations (in the "other_names" list for every station)
            for caltrain_station, value in caltrain_other_stations.items():
                if station["Name"] in value["other_names"]:
                    print(f"Found {station['Name']} in caltrain_other_stations")
                    print(caltrain_station)
                    print(value)
                    # get the caltrain station
                    found = False
                    for old_station in old_ct_data:
                        if old_station["id"] == caltrain_station:
                            caltrain_station = old_station
                            found = True
                            break
                    assert found, f"Could not find {caltrain_station} in old_ct_data"

                    # add line_id to connections
                    # Check if line_id is already in connections
                    if line_id in caltrain_station["connections"]:
                        print(f"Line {line_id} already in connections")
                        break
                    print(f"Adding {line_id} to connections")
                    caltrain_station["connections"].append(line_id)
                    # caltrain_station['operator'] = 'SC'
                    print (caltrain_station)
                    break


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

    # Check Santa Clara Caltrain Station connections
    for station in old_ct_data:
        if station["id"] == "70241":
            print(station)

    
    with open("stations_ct.json", "w") as f:
        json.dump(old_ct_data, f, indent=4)

    with open("stations_vta.json", "w") as f:
        json.dump(old_vta_data, f, indent=4)

    with open("stations_sfo.json", "w") as f:
        json.dump(old_sfo_data, f, indent=4)