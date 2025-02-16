
# Input: geojson
# Output: same geojson with lat and lon flipped

def coord_switch(geojson):
    for feature in geojson["features"]:
        for i in range(len(feature["geometry"]["coordinates"])):
            feature["geometry"]["coordinates"][i] = feature["geometry"]["coordinates"][i][
                ::-1
            ]
    return geojson

# Input: shapes/CE.geojson

# Output: updated_CE.geojson with lat and lon flipped
if name == "__main__":
    import json
    with open("shapes/CE.geojson") as f:
        geojson = json.load(f)

    updated_geojson = coord_switch(geojson)

    with open("updated_CE.geojson", "w") as f:
        json.dump(updated_geojson, f)

    