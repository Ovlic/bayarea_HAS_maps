
import os
# Input: geojson
# Output: same geojson with lat and lon flipped

def switch_coords(geojson):
    for feature in geojson["features"]:
        for i in range(len(feature["geometry"]["coordinates"])):
            # if len(feature["geometry"]["coordinates"][i]) == 1:
            #     for j in range(len(feature["geometry"]["coordinates"][i])):
            #         feature["geometry"]["coordinates"][i][j] = feature["geometry"]["coordinates"][i][j][
            #             ::-1
            #         ]
            feature["geometry"]["coordinates"][i] = feature["geometry"]["coordinates"][i][
                ::-1
            ]
    return geojson

# Example usage:
# Input: CE.geojson
# Output: updated_CE.geojson with lat and lon flipped
if __name__ == "__main__":
    import json
    # Loop through files in data/qgis_track_data and flip the coordinates
    """
    for filename in os.listdir("data/qgis_track_data/bart"):
        if not filename.endswith(".geojson"):
            continue
        print(f"Processing {filename}")
        with open(f"data/qgis_track_data/bart/{filename}") as f:
            geojson = json.load(f)

        updated_geojson = switch_coords(geojson)

        
        with open(f"data/track_data/bart/{filename}", "w") as f:
            json.dump(updated_geojson, f)
        
        print("Done")
        """
    files = ["blue_line.geojson", "red_line.geojson"]
    for filename in files:
        with open(f"data/qgis_track_data/sfo/{filename}") as f:
            geojson = json.load(f)

        updated_geojson = switch_coords(geojson)

        with open(f"data/track_data/sfo/{filename}", "w") as f:
            json.dump(updated_geojson, f)
    
    # """
    