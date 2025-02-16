
import json


with open('shapes.json') as f:
    shapes = json.load(f)

# Load colors
with open('colors.json') as f:
    colors = json.load(f)


# Shapes format: { "trip_id": [ [lat, lon], [lat, lon], ... ] }"}
# Convert shapes to geojson format
for operator in shapes:
    if operator == "BA": 
        continue
    if operator == "CT":
        continue
    shapes_geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for trip_id, coords in shapes[operator].items():
        # Reverse coordinates
        # If the coordinates are in the format [lat, lon], swap them to [lon, lat]
        print(f"operator: {operator}; coords_len: {len(coords)}")
        for coord in coords:
            try:
                coord[0]
            except:
                print("Error!")
                # print(coords)
            if isinstance(coords, list):
                print(coord)
                coord[0], coord[1] = coord[1], coord[0]
            else:
                # Coords are in format "lat,lon"
                # Reverse
                coord_raw = coord.split(",")
                print(coord_raw)
                coord = [float(coord_raw[1]), float(coord_raw[0])]
        #for coord in coords:
            # Reverse coordinates
            #coord[0], coord[1] = coord[1], coord[0]
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


    with open(f'export/shapes/{operator}.geojson', 'w') as f:
        json.dump(shapes_geojson, f)