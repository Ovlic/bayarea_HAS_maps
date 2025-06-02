
# Draws the tracks from geojson files pulled from OpenStreetMap
import json, folium
from folium.plugins import FeatureGroupSubGroup

def draw_tracks(m:folium.Map):
    n_dt = ["way/25025892", "way/160312612", "way/160312613", "way/160312615", "way/427294307", "way/427294308", "way/556413439", "way/556413440", "way/740756378"]
    t_dt = ["way/1128011243", "way/1128011244"]

    data_path = "data/"

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
        j_line_crossovers_raw = json.load(f)
        j_line_crossovers = [track['properties']['id'] for track in j_line_crossovers_raw['features']]
        

    with open(data_path + 'track_data/k_line_crossovers.geojson') as f:
        k_line_crossovers_raw = json.load(f)
        k_line_crossovers = [track['properties']['id'] for track in k_line_crossovers_raw['features']]


    with open(data_path + 'track_data/l_line_crossovers.geojson') as f:
        l_line_crossovers_raw = json.load(f)
        l_line_crossovers = [track['properties']['id'] for track in l_line_crossovers_raw['features']]

    with open(data_path + 'track_data/m_line_crossovers.geojson') as f:
        m_line_crossovers_raw = json.load(f)
        m_line_crossovers = [track['properties']['id'] for track in m_line_crossovers_raw['features']]

    with open(data_path + 'track_data/n_line_crossovers.geojson') as f:
        n_line_crossovers_raw = json.load(f)
        n_line_crossovers = [track['properties']['id'] for track in n_line_crossovers_raw['features']]

    with open(data_path + 'track_data/t_line_crossovers.geojson') as f:
        t_line_crossovers_raw = json.load(f)
        t_line_crossovers = [track['properties']['id'] for track in t_line_crossovers_raw['features']]

    with open(data_path + 'track_data/california_cable_car.geojson') as f:
        ccc_raw = json.load(f)
        ccc = [track['properties']['id'] for track in ccc_raw['features']]

    with open(data_path + 'track_data/powell_hyde_cable_car.geojson') as f:
        phc_raw = json.load(f)
        phc = [track['properties']['id'] for track in phc_raw['features']]

    with open(data_path + 'track_data/powell_mason_cable_car.geojson') as f:
        pmc_raw = json.load(f)
        pmc = [track['properties']['id'] for track in pmc_raw['features']]

    with open(data_path + 'track_data/muni_38R.geojson') as f:
        muni_38r = json.load(f)

    with open(data_path + 'track_data/oak_connector.geojson') as f:
        oak_connector = json.load(f)

    with open(data_path + "colors.json") as f:
        colors = json.load(f)

    # Bart, Muni, and NULL tracks should be FeatureGroupSubGroups
    bart_tracks = folium.FeatureGroup(name="BART Tracks", interactive=False)
    # Make BART feature groups for each line
    bart_r = folium.FeatureGroup(name="Red")
    bart_g = folium.FeatureGroup(name="Green")
    bart_o = folium.FeatureGroup(name="Orange")
    bart_b = folium.FeatureGroup(name="Blue")
    bart_y = folium.FeatureGroup(name="Yellow")
    bart_oak = folium.FeatureGroup(name="OAK Connector")

    # Make Muni feature groups for each line
    muni_tracks = folium.FeatureGroup(name="Muni Tracks", show=True)
    # Test featuregroupsubgroup in another featuregroupsubgroup for cable cars
    muni_f = folium.FeatureGroup(name="F", show=True)
    muni_j = folium.FeatureGroup(name="J", show=True)
    muni_k = folium.FeatureGroup(name="K", show=True)
    muni_l = folium.FeatureGroup(name="L", show=True)
    muni_m = folium.FeatureGroup(name="M", show=True)
    muni_n = folium.FeatureGroup(name="N", show=True)
    muni_t = folium.FeatureGroup(name="T", show=True)
    # Cable Cars
    cable_cars = folium.FeatureGroup(name="Cable Cars", show=True)
    cc_ca = folium.FeatureGroup(name="California Cable Car", show=True)
    cc_pm = folium.FeatureGroup(name="Powell-Mason Cable Car", show=True)
    cc_ph = folium.FeatureGroup(name="Powell-Hyde Cable Car", show=True)
    # Buses
    buses = folium.FeatureGroup(name="Buses", show=True)
    bus_38r = folium.FeatureGroup(name="38R", show=True)


    null_tracks = folium.FeatureGroup(name="NULL Tracks", show=False)

    layers = {
        "BA": {
            "Red": bart_r,
            "Green": bart_g,
            "Orange": bart_o,
            "Blue": bart_b,
            "Yellow": bart_y,
            "OAK": bart_oak
        },
        "SF": {
            "F": muni_f,
            "J": muni_j,
            "K": muni_k,
            "L": muni_l,
            "M": muni_m,
            "N": muni_n,
            "T": muni_t,
            "CA": cc_ca,
            "PM": cc_pm,
            "PH": cc_ph,
            "038R": bus_38r
        }
    }


    # bart_tracks = folium.FeatureGroup(name="BART Tracks")
    # muni_tracks = folium.FeatureGroup(name="Muni Tracks")
    # # Add a feature group for NULL tracks that only shows up when zoomed in enough
    # null_tracks = folium.FeatureGroup(name="NULL Tracks", show=False)


    # Add the tracks (color based on their name and network)

    for track in data['features']:
        if track['properties']['network'] == "BART":
            print("BART")
            # "R-Line" "M-Line" "L-Line" "K-Line" "C-Line" "Bay Area Rapid Transit Railroad" "BART Silicon Valley Phase I" "BART Berryessa Extension" "BART" "A-Line"

            # Yellow = "Y-Line", "C-Line"
            # Red = "W-Line", "BART"
            # Green = "M-Line", "A-Line", "S-Line", "BART Silicon Valley Phase I", "BART Berryessa Extension"
            # Orange = "R-Line", "K-Line" # Might adjust the k line since its where 12h & 19th are
            # Blue = "L-Line"
            # Gray = NULL
            name = track['properties']['name']
            line = ""
            if name in ["R-Line", "K-Line"]:
                color = colors["BA"]["Orange-N"]
                line = "Orange"
            elif name in ["M-Line", "A-Line", "S-Line", "BART Silicon Valley Phase I", "BART Berryessa Extension"]:
                # Loop through test_dc and compare ids to see if the track is in the past_dc, if it is color it red
                found = False
                for dc in past_dc['features']:
                    if dc['properties']['id'] == track['properties']['id']:
                        color = colors["BA"]["Red-N"]
                        line = "Red"
                        found = True
                        break
                if not found:
                    color = colors["BA"]["Green-N"]
                    line = "Green"
            elif name in ["L-Line"]:
                color = colors["BA"]["Blue-N"]
                line = "Blue"
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
                    line = "Red"
            elif name in ["Y-Line", "C-Line"]:
                color = colors["BA"]["Yellow-N"]
                line = "Yellow"
            else:
                color = "#808080"

            # Add null tracks to the null_tracks feature group
            if color == "#808080":
                folium.PolyLine(
                    locations=track['geometry']['coordinates'],
                    color=color,
                    weight=2,
                    name=name,
                    popup=f"<b>{name}</b>; {track['properties']['network']}; {track['properties']['layer']}"
                ).add_to(null_tracks)
            else:
                folium.PolyLine(
                    locations=track['geometry']['coordinates'],
                    color=color,
                    weight=4,
                    name=name,
                    popup=f"<b>{name}</b>;"#{track['properties']['network']}; {track['properties']['layer']}"# Name, network
                ).add_to(layers["BA"][line])

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
            line = ""
            if name in ["Muni L"] or track['properties']['id'] in l_line_crossovers:
                color = colors["SF"]["L"]
                line = "L"
            elif name in ["Muni N", "Muni N / Sunset Tunnel"] or track['properties']['id'] in n_line_crossovers:
                color = colors["SF"]["N"]
                line = "N"
            elif name in ["Muni T"] or track['properties']['id'] in t_line_crossovers:
                color = colors["SF"]["T"]
                line = "T"
            elif name in ["Muni J"] or track['properties']['id'] in j_line_crossovers:
                color = colors["SF"]["J"]
                line = "J"
            elif name in ["Muni K"] or track['properties']['id'] in k_line_crossovers:
                color = colors["SF"]["K"]
                line = "K"
            elif name in ["Muni F"] or track['properties']['id'] in ['way/556413443']:
                color = colors["SF"]["F"]
                line = "F"
            elif name in ["Muni M", "Muni Metro / Twin Peaks Tunnel"]:
                color = colors["SF"]["M"]
                line = "M"
            
            # Part of the E line and part of the F line share tracks, with the E line being the primary line. Since the E is not running, we will color the shared tracks pink and add them to null_tracks. The F line will be colored normally.
            elif name in ["Muni E"]:
                found = False
                for e in muni_e['features']:
                    if e['properties']['id'] == track['properties']['id']:
                        # E line!
                        color = "#f542b0"
                        found = True
                        break
                if not found:
                    # Its the F line
                    color = colors["SF"]["F"]
                    line = "F"

            elif name in ["Muni Metro"]:
                if track['properties']['id'] in n_dt:
                    # N line running on the Embarcadero
                    color = colors["SF"]["N"]
                    line = "N"
                elif track['properties']['id'] in t_dt:
                    # Part of the T line running by the Caltrain station has the Muni Metro name for some reason
                    color = colors["SF"]["T"]
                    line = "T"
                else:
                    if track['properties']['id'] in ["way/160312616", "way/26786374"]: 
                        color = "#808080"
                    # Give color based on the level property (if the level is NULL, it gets the N color, else it gets the K color)
                    elif track['properties']['level'] == None:
                        if track['properties']['maxspeed'] == None:
                            color = colors["SF"]["M"]
                            line = "M"
                        else:
                            # The N splitting off from the other lines at Duboce
                            if track['properties']['layer'] == None or track['properties']['layer'] == "-2" or track['properties']['id'] == "way/160307216":
                                color = colors["SF"]["N"]
                                line = "N"
                                # FIXME: This is where the N and J come aboveground, but also its part of the N on the embarcadero.
                            else:
                                # Muni Metro running on Market (colored the same as the K line)
                                color = colors["SF"]["K"]
                                line = "K"
                    elif track['properties']['level'] == "-2":
                        # Muni Metro running on Market (colored the same as the K line)
                        color = colors["SF"]["K"]
                        line = "K"
                    else:
                        # Any other track
                        color = "#808080"
            elif name in ["Central Subway Northbound", "Central Subway Southbound"]:
                # Central Subway future expansion
                if track['properties']['start_date'] == None:
                    color = "#808080"
                else:
                    # T line running on the Central Subway
                    color = colors["SF"]["T"]
                    line = "T"
            else:
                if track['properties']['gauge'] == "1067":
                    # Cable car tracks
                    # color = "#f542b0"
                    if track['properties']['id'] in ccc:
                        color = colors["SF"]["CA"]
                        line = "CA"
                    elif track['properties']['id'] in pmc:
                        color = colors["SF"]["PM"]
                        line = "PM"
                    elif track['properties']['id'] in phc:
                        color = colors["SF"]["PH"]
                        line = "PH"

                    else:
                        color = "#808080"
                    
                else:
                    color = "#808080"

            if color in ['#f542b0', '#808080']:
                # Add to null_tracks
                folium.PolyLine(
                    locations=track['geometry']['coordinates'],
                    color=color,
                    weight=2,
                    name=name,
                    popup=f"<b>{name}</b>; {track['properties']['network']}; {track['properties']['railway']}; {track['properties']['layer']}; {track['properties']['id']}",
                ).add_to(null_tracks)
            else:
                folium.PolyLine(
                    locations=track['geometry']['coordinates'],
                    color=color,
                    weight=4,
                    name=name,
                    popup=f"<b>{name}</b>; {track['properties']['network']}; {track['properties']['railway']}; {track['properties']['layer']}; {track['properties']['id']}", # Name, network
                    smooth_factor=1
                ).add_to(layers["SF"][line])

        else:
            print("NULL")
            folium.PolyLine(
                locations=track['geometry']['coordinates'],
                color="#808080",
                weight=2,
                name="NULL"
            ).add_to(m)# .add_to(null_tracks)

    # Add 38R
    for track in muni_38r['features']:
        folium.PolyLine(
            locations=track['geometry']['coordinates'],
            color=colors["SF"]["038R"],
            weight=4,
            name="Muni 38R",
            popup=f"<b>Muni 38R</b>; {track['properties']['network']}; {track['properties']['railway']}; {track['properties']['layer']}; {track['properties']['id']}", # Name, network
            smooth_factor=1
        ).add_to(bus_38r)

    # Add the oak connector
    for track in oak_connector['features']:
        folium.PolyLine(
            locations=track['geometry']['coordinates'],
            color=colors["BA"]["Beige-N"],
            weight=4,
            name="OAK Connector",
            popup=f"<b>OAK Connector</b>; {track['properties']['network']}; {track['properties']['railway']}; {track['properties']['layer']}; {track['properties']['id']}", # Name, network
            smooth_factor=1
        ).add_to(bart_oak)

    # Add the platforms
    # Do later

    # print(bart_tracks.to_dict())
    # Add the feature groups to the map
    m.add_child(bart_tracks)
    for line in layers["BA"]:
        m.add_child(layers["BA"][line])

    m.add_child(muni_tracks)
    for line in layers["SF"]:
        m.add_child(layers["SF"][line])
    m.add_child(null_tracks)


if __name__ == "__main__":
    m = folium.Map(
        location=[37.7749, -122.4194],
        zoom_start=12,
        tiles='cartodbpositron'
        )

    draw_tracks(m)
    # Add a layer control
    m.add_child(folium.LayerControl())

    # Save the map
    filepath = 'local/muni_tracks.html'
    m.save(filepath)
    print(f"Saved to {filepath}")
