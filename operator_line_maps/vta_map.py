
import json, folium, transit_map

with open("data/track_data/vta/blue_line.geojson") as f:
    blue_line = json.load(f)

with open("data/track_data/vta/green_line.geojson") as f:
    green_line = json.load(f)

with open("data/track_data/vta/orange_line.geojson") as f:
    orange_line = json.load(f)

with open("data/colors.json") as f:
    colors = json.load(f)


m = folium.Map(location=[37.3, -121.9], zoom_start=11, tiles="cartodbpositron")

for feature in blue_line["features"]:
    folium.PolyLine(
        locations=feature["geometry"]["coordinates"], 
        color=colors['SC']['Blue Line'],
        tooltip="Blue Line",
        name="Blue Line",
        width=4
    ).add_to(m)

for feature in green_line["features"]:
    folium.PolyLine(
        locations=feature["geometry"]["coordinates"], 
        color=colors['SC']['Green Line'],
        tooltip="Green Line",
        name="Green Line",
        width=4
    ).add_to(m)

for feature in orange_line["features"]:
    folium.PolyLine(
        locations=feature["geometry"]["coordinates"], 
        color=colors['SC']['Orange Line'],
        tooltip="Orange Line",
        name="Orange Line",
        width=4
    ).add_to(m)

m.save("local/vta_map.html")
