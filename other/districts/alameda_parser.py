
# Filter through Alameda_City_Council_Districts.geojson and extract features and print their names

import json

with open("Alameda_City_Council_Districts.geojson") as f:
    alameda = json.load(f)

sub_geojsons = {}
for feature in alameda["features"]:
    print(feature["properties"]["DIST_NAME"])
    city = feature["properties"]["DIST_NAME"].split("CITY OF ")[1].split(",")[0]
    print(city)
    if city not in sub_geojsons:
        sub_geojsons[city] = {"type": "FeatureCollection", "features": []}
    sub_geojsons[city]["features"].append(feature)

# Loop through sub_geojsons and write each one to a new file (name it after the city in lowercase)
for city, geojson in sub_geojsons.items():
    with open(f"alameda/{city.lower()}.geojson", "w") as f:
        json.dump(geojson, f)