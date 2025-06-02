
import json, folium, transit_map

with open("data/track_data/sfo/blue_line.geojson") as f:
    blue_line = json.load(f)

with open("data/track_data/sfo/red_line.geojson") as f:
    red_line = json.load(f)


with open("data/colors.json") as f:
    colors = json.load(f)


m = folium.Map(location=[37.3, -121.9], zoom_start=11, tiles="cartodbpositron")

for feature in blue_line["features"]:
    folium.PolyLine(
        locations=feature["geometry"]["coordinates"], 
        color=colors['SI']['Blue Line AirTrain'],
        tooltip="Blue Line AirTrain",
        name="Blue Line AirTrain",
        width=4
    ).add_to(m)

for feature in red_line["features"]:
    folium.PolyLine(
        locations=feature["geometry"]["coordinates"], 
        color=colors['SI']['Red Line AirTrain'],
        tooltip="Red Line AirTrain",
        name="Red Line AirTrain",
        width=4
    ).add_to(m)


m.save("local/sfo_map.html")
