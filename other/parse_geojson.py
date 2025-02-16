
import json

# Load data from JSON files
with open("Muni Simple Routes_20250125.geojson", "r") as f:
    muni_routes = json.load(f)

new_muni_routes = {
    "type": "FeatureCollection",
    "features": []
}
# Filter out everything that does not have a "service_ca" of either "Cable Car", "Muni Metro", or "Historic" within the "properties" key
for i in range(len(muni_routes["features"])):
    if muni_routes["features"][i]["properties"]["service_ca"] in ["Cable Car", "Muni Metro", "Historic"]:
        new_muni_routes["features"].append(muni_routes["features"][i])

# Save the filtered data to a new JSON file
with open("filtered_muni_routes.geojson", "w") as f:
    # Dump into file with tab indentation
    json.dump(new_muni_routes, f, indent=4)