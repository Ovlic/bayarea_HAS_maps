
import json

# Load data from files
with open('filtered_muni_routes.geojson') as f:
    muni = json.load(f)

with open('caltrain.geojson') as f:
    caltrain = json.load(f)

with open('sf.geojson') as f:
    sf = json.load(f)

with open('shapes.json') as f:
    shapes = json.load(f)

# Load colors
with open('colors.json') as f:
    colors = json.load(f)


# Update colors for muni (based on lineabbr)
for feature in muni['features']:
    feature['properties']['color'] = colors["SF"][feature['properties']['lineabbr']]

# Update colors for caltrain
for feature in caltrain['features']:
    feature['properties']['color'] = colors['CT']['Express']

# Update colors for sf
for feature in sf['features']:
    feature['properties']['color'] = "#FF0000"

# Only keep data within "BA"
shapes = shapes["BA"]
# Shapes format: { "trip_id": [ [lat, lon], [lat, lon], ... ] }"}
# Convert shapes to geojson format
shapes_geojson = {
    "type": "FeatureCollection",
    "features": []
}

for trip_id, coords in shapes.items():
    for coord in coords:
        # Reverse coordinates
        coord[0], coord[1] = coord[1], coord[0]
    shapes_geojson["features"].append({
        "type": "Feature",
        "properties": {
            "trip_id": trip_id
        },
        "geometry": {
            "type": "LineString",
            "coordinates": coords
        }
    })

# Save updated data in export folder with same file names
# Create folder if it doesn't exist
import os
if not os.path.exists('export'):
    os.makedirs('export')


with open('export/filtered_muni_routes.geojson', 'w') as f:
    json.dump(muni, f)

with open('export/caltrain.geojson', 'w') as f:
    json.dump(caltrain, f)

with open('export/sf.geojson', 'w') as f:
    json.dump(sf, f)

with open('export/bart.geojson', 'w') as f:
    json.dump(shapes_geojson, f)