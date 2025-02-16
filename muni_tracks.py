
import json, folium

n_dt = ["way/25025892", "way/160312612", "way/160312613", "way/160312615", "way/427294307", "way/427294308", "way/556413439", "way/556413440", "way/740756378"]
t_dt = ["way/1128011243", "way/1128011244"]

data_path = "data"

# Load the data
with open(data_path + 'track_data/updated_muni_tracks.geojson') as f:
    data = json.load(f)

with open(data_path + 'track_data/muni_platforms.geojson') as f:
    platforms = json.load(f)

with open(data_path + 'track_data/test_past_dc.geojson') as f:
    past_dc = json.load(f)

with open(data_path + 'track_data/past_millbrae.geojson') as f:
    past_millbrae = json.load(f)

with open(data_path + 'track_data/n_downtown.geojson') as f:
    n_downtown = json.load(f)
    for feature in n_downtown['features']:
        # Add the feature to n_dt if it is not already in there
        if feature['properties']['id'] not in n_dt:
            n_dt.append(feature['properties']['id'])

with open(data_path + 'track_data/muni_e.geojson') as f:
    muni_e = json.load(f)

with open(data_path + 'track_data/j_line_crossovers.geojson') as f:
    j_line_crossovers = json.load(f)

with open(data_path + 'track_data/k_line_crossovers.geojson') as f:
    k_line_crossovers = json.load(f)

with open(data_path + 'track_data/l_line_crossovers.geojson') as f:
    l_line_crossovers = json.load(f)

with open(data_path + 'track_data/m_line_crossovers.geojson') as f:
    m_line_crossovers = json.load(f)

with open(data_path + 'track_data/n_line_crossovers.geojson') as f:
    n_line_crossovers = json.load(f)

with open(data_path + 'track_data/t_line_crossovers.geojson') as f:
    t_line_crossovers = json.load(f)

with open(data_path + "colors.json") as f:
    colors = json.load(f)


# Create a map centered at San Francisco
m = folium.Map(
    location=[37.7749, -122.4194],
    zoom_start=12,
    tiles='cartodbpositron'
    )

bart_tracks = folium.FeatureGroup(name="BART Tracks")
muni_tracks = folium.FeatureGroup(name="Muni Tracks")
# Add a feature group for NULL tracks that only shows up when zoomed in enough
null_tracks = folium.FeatureGroup(name="NULL Tracks", show=False)


# Add the tracks (color based on their name and network)

for track in data['features']:
    if track['properties']['network'] == "BART":
        print("BART")
        "R-Line" "M-Line" "L-Line" "K-Line" "C-Line" "Bay Area Rapid Transit Railroad" "BART Silicon Valley Phase I" "BART Berryessa Extension" "BART" "A-Line"
        # Yellow = "Y-Line", "C-Line"
        # Red = "W-Line", "BART"
        # Green = "M-Line", "A-Line", "S-Line", "BART Silicon Valley Phase I", "BART Berryessa Extension"
        # Orange = "R-Line", "K-Line" # Might adjust the k line since its where 12h & 19th are
        # Blue = "L-Line"
        # Gray = NULL
        name = track['properties']['name']
        if name in ["R-Line", "K-Line"]:
            color = colors["BA"]["Orange-N"]
        elif name in ["M-Line", "A-Line", "S-Line", "BART Silicon Valley Phase I", "BART Berryessa Extension"]:
            # Loop through test_dc and compare ids to see if the track is in the past_dc, if it is color it red
            found = False
            for dc in past_dc['features']:
                if dc['properties']['id'] == track['properties']['id']:
                    color = colors["BA"]["Red-N"]
                    found = True
                    break
            if not found:
                color = colors["BA"]["Green-N"]
        elif name in ["L-Line"]:
            color = colors["BA"]["Blue-N"]
        elif name in ["W-Line", "BART"]:
            # Loop through test_millbrae and compare ids to see if the track is in the past_millbrae, if it is color it gray
            found = False
            for millbrae in past_millbrae['features']:
                if millbrae['properties']['id'] == track['properties']['id']:
                    color = "#808080"
                    found = True
                    break
            if not found:
                color = colors["BA"]["Red-N"]
        elif name in ["Y-Line", "C-Line"]:
            color = colors["BA"]["Yellow-N"]
        else:
            color = "#808080"

        folium.PolyLine(
            locations=track['geometry']['coordinates'],
            color=color,
            weight=4,
            name=name,
            popup=f"<b>{name}</b>; {track['properties']['network']}; {track['properties']['layer']}"# Name, network
        ).add_to(bart_tracks)

    elif track['properties']['network'] == "Muni":
        print("Muni")
        # L = "Muni L"
        # N = "Muni N", "Muni N / Sunset Tunnel"
        # T = "Muni T"
        # J = "Muni J"
        # K = "Muni K"
        # F = "Muni F"
        # M = "Muni M", "Muni Metro / Twin Peaks Tunnel"

        # Test
        # E = "#f542b0"
        # Gray = NULL, "Muni", "Muni Metro"

        name = track['properties']['name']
        if name in ["Muni L"]:
            color = colors["SF"]["L"]
        elif name in ["Muni N", "Muni N / Sunset Tunnel"]:
            color = colors["SF"]["N"]
        elif name in ["Muni T"]:
            color = colors["SF"]["T"]
        elif name in ["Muni J"]:
            color = colors["SF"]["J"]
        elif name in ["Muni K"]:
            color = colors["SF"]["K"]
        elif name in ["Muni F"]:
            color = colors["SF"]["F"]
        elif name in ["Muni M", "Muni Metro / Twin Peaks Tunnel"]:
            color = colors["SF"]["M"]
        elif name in ["Muni E"]:
            found = False
            for e in muni_e['features']:
                if e['properties']['id'] == track['properties']['id']:
                    color = "#f542b0"
                    found = True
                    break
            if not found:
                # Its the F line
                color = colors["SF"]["F"]
        elif name in ["Muni Metro"]:
            if track['properties']['id'] in n_dt:
                color = colors["SF"]["N"]
            elif track['properties']['id'] in t_dt:
                color = colors["SF"]["T"]
            else:
                # Give color based on the level property (if the level is NULL, it gets the N color, else it gets the K color)
                if track['properties']['level'] == None:
                    if track['properties']['maxspeed'] == None:
                        color = colors["SF"]["M"]
                    else:
                        if track['properties']['layer'] == None or track['properties']['layer'] == "-2" or track['properties']['id'] == "way/160307216":
                            color = colors["SF"]["N"]
                        else:
                            color = colors["SF"]["K"]
                elif track['properties']['level'] == "-2":
                    color = colors["SF"]["K"]
                else:
                    
                    color = "#808080"
        elif name in ["Central Subway Northbound", "Central Subway Southbound"]:
            if track['properties']['start_date'] == None:
                color = "#808080"
            else:
                color = colors["SF"]["T"]
        else:
            if track['properties']['gauge'] == "1067":
                color = "#f542b0"
            else:
                color = "#808080"

        folium.PolyLine(
            locations=track['geometry']['coordinates'],
            color=color,
            weight=4,
            name=name,
            popup=f"<b>{name}</b>; {track['properties']['network']}; {track['properties']['railway']}; {track['properties']['layer']}", # Name, network
            smooth_factor=1
        ).add_to(muni_tracks)

    else:
        print("NULL")
        folium.PolyLine(
            locations=track['geometry']['coordinates'],
            color="#808080",
            weight=2,
            name="NULL"
        ).add_to(m)# .add_to(null_tracks)

# Add the platforms
# Do later

# print(bart_tracks.to_dict())
# Add the feature groups to the map
m.add_child(bart_tracks)
m.add_child(muni_tracks)
m.add_child(null_tracks)

# Add a layer control
m.add_child(folium.LayerControl())

# Save the map
m.save('local/muni_tracks.html')
