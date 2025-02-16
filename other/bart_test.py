
# Create a folium map of the BART system in the San Francisco Bay Area using the files in "bart_data" folder

import json, folium

class Shape(object):
    """
    shape_id,shape_pt_lon,shape_pt_lat,shape_pt_sequence,shape_dist_traveled
    p_1277284,-121.5661454201,37.003512298,1,0.00000000
"""
    def __init__(self, data):
        self.__data = data

    @property
    def shape_id(self):
        return self.__data[0]

    @property
    def shape_pt_lon(self):
        return self.__data[1]

    @property
    def shape_pt_lat(self):
        return self.__data[2]

    @property
    def shape_pt_sequence(self):
        return self.__data[3]

    @property
    def shape_dist_traveled(self):
        return self.__data[4]

def convert_shape_gtfs_to_shape(shape_gtfs):
    shape_gtfs = shape_gtfs.split("\n")[1:]
    shape_gtfs = [Shape(x.split(",")) for x in shape_gtfs]
    return shape_gtfs


m = folium.Map(
    #location=[37.65077186632317, -122.24094250022335],
    #zoom_start=9,
    location=[37.7545, -122.4425],
    zoom_start=12,
    # zoom_control=False,
    # attributionControl=False,
    tiles="cartodbpositron"
    )

# Load data from files
with open("GTFSTransitData_CE/shapes.txt") as f:
    shapes = f.read()

shapes = convert_shape_gtfs_to_shape(shapes)
shape_ids = list(set([x.shape_id for x in shapes]))

# The only shape id we want to show is "pv35"
for shape_id in shape_ids:
    if shape_id != "pv35":
        continue
    line = [x for x in shapes if x.shape_id == shape_id]
    line_coords = [(float(x.shape_pt_lat), float(x.shape_pt_lon)) for x in line]
    print(line_coords)
    folium.PolyLine(
        line_coords,
        color="#FF0000",
        tooltip=line[0].shape_id,
    ).add_to(m)
    

m.save("ace_map.html")


# Convert shapes to geojson format
geojson = {
    "type": "FeatureCollection",
    "features": []
}

for shape_id in shape_ids:
    if shape_id != "pv35":
        continue
    line = [x for x in shapes if x.shape_id == shape_id]
    line_coords = [(float(x.shape_pt_lon), float(x.shape_pt_lat)) for x in line]
    geojson["features"].append({
        "type": "Feature",
        "properties": {
            "shape_id": shape_id
        },
        "geometry": {
            "type": "LineString",
            "coordinates": line_coords
        }
    })

print("Saving geojson")
with open("ace.geojson", "w") as f:
    json.dump(geojson, f)
