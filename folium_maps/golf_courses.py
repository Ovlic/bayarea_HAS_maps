

# Data sourced from: https://www.golftrips.com/golfmap/sanfrancisco
# Load from data/tentacles_data/golf_courses.geojson

import folium, json
import transit_map

# Load the data
with open('data/tentacles_data/golf_courses.geojson') as f:
    golf_courses = json.load(f)
with open('data/tentacles_data/mountains.geojson') as f:
    mountains = json.load(f)

hills = {
    "type": "FeatureCollection",
    "features": []
}


m = folium.Map(
    location=[37.7749, -122.4194], 
    zoom_start=12,
    tiles="cartodbpositron"
    )  # Default to San Francisco

transit_map.add_tiles(m)


# public_fg = folium.FeatureGroup(name="Public Golf Courses")
# private_fg = folium.FeatureGroup(name="Private Golf Courses")
golf_fg = folium.FeatureGroup(name="Golf Courses")
airport_fg = folium.FeatureGroup(name="Airports")
# Add airports
folium.Marker(
    location=[37.62298345677303, -122.38205306910905],  # SFO
    popup=folium.Popup(
        "<b>Name</b>: San Francisco International Airport",
        max_width=265
    ),
    icon=folium.Icon(color="lightgray", icon="plane", prefix="fa")
).add_to(airport_fg)
folium.Marker(
    location=[37.72277228787828, -122.21940375153538],  # OAK
    popup=folium.Popup(
        "<b>Name</b>: Oakland International Airport",
        max_width=265
    ),
    icon=folium.Icon(color="lightgray", icon="plane", prefix="fa")
).add_to(airport_fg)

for golf_course in golf_courses['features']:
    if golf_course["properties"]["type"] == "public":
        folium.Marker(
            location = [
                golf_course["geometry"]["coordinates"][1],
                golf_course["geometry"]["coordinates"][0]
            ],
            # Popup with name and type
            # Like this: "**name**: name-here\n**type**: type-here"
            # ** is bold in markdown, make it bold in the popup
            popup = folium.Popup(
                f"<b>Name</b>: {golf_course['properties']['name']}<br><b>Type</b>: {golf_course['properties']['type']}",
                max_width=265
            ),
            icon = folium.Icon(
                color="darkgreen", 
                icon="golf-ball-tee", 
                prefix="fa"
            )
        ).add_to(golf_fg)#(public_fg)
    else:
        folium.Marker(
            location = [
                golf_course["geometry"]["coordinates"][1],
                golf_course["geometry"]["coordinates"][0]
            ],
            popup = folium.Popup(
                f"<b>Name</b>: {golf_course['properties']['name']}<br><b>Type</b>: {golf_course['properties']['type']}",
                max_width=265
            ),
            icon = folium.Icon(
                color="darkgreen", 
                icon="golf-ball-tee", 
                prefix="fa"
            )
        ).add_to(golf_fg)#(private_fg)


mountains_fg = folium.FeatureGroup(name="Mountains")
hills_fg = folium.FeatureGroup(name="Hills")
no_name_fg = folium.FeatureGroup(name="No Name")

for mountain in mountains['features']:
    if 'name' not in mountain['properties']:
        continue
    if 'hill' not in mountain['properties']['name'].lower():
        folium.Marker(
            location = [
                mountain["geometry"]["coordinates"][1],
                mountain["geometry"]["coordinates"][0]
            ],
            popup = mountain["properties"]["name"],
            icon = folium.Icon(
                color="red", 
                icon="mountain", 
                prefix="fa"
            )
        ).add_to(mountains_fg)


mountains_fg.add_to(m)

# public_fg.add_to(m)
# private_fg.add_to(m)
golf_fg.add_to(m)
# Add airports to the map
airport_fg.add_to(m)

# Add sf borders
transit_map.add_sf_boundary(m)

# Add a layer control
transit_map.add_plugins(m)

m.save('local/golf_courses_map.html')
transit_map.add_favicons(filename='local/golf_courses_map.html')