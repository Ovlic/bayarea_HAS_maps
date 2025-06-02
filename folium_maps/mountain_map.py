
# Load from data/tentacles_data/mountains.geojson

import folium, json
import transit_map

# Load the data
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




# # Add mountains to map
# folium.GeoJson(
#     mountains,
#     name='mountains',
#     tooltip=folium.GeoJsonTooltip(fields=['name']),
#     # Popup is the same as tooltip
#     popup = folium.GeoJsonPopup(
#         fields=['name'],
#         aliases=['Mountain Name']
#     ),
#     marker=folium.Marker(
#         icon=folium.Icon(
#             color="red",
#             icon="mountain",
#             prefix="fa"
#         )
#     ),
#     style_function=lambda x: {
#         'fillColor': 'transparent',
#         'color': '#FF0000',
#         'weight': 2
#     }
# ).add_to(m)

# # Add hills to map
# folium.GeoJson(
#     hills,
#     name='hills',
#     tooltip=folium.GeoJsonTooltip(fields=['name']),
#     # Popup is the same as tooltip
#     popup = folium.GeoJsonPopup(
#         fields=['name'],
#         aliases=['Hill Name']
#     ),
#     marker=folium.Marker(
#         icon=folium.Icon(
#             color="blue",
#             icon="mound",
#             prefix="fa"
#         )
#     )
# ).add_to(m)

mountains_fg = folium.FeatureGroup(name="Mountains")
hills_fg = folium.FeatureGroup(name="Hills")
no_name_fg = folium.FeatureGroup(name="No Name")

for mountain in mountains['features']:
    if 'name' not in mountain['properties']:
        print("No name in mountain")
        folium.Marker(
            location = [
                mountain["geometry"]["coordinates"][1],
                mountain["geometry"]["coordinates"][0]
            ],
            popup = "No name",
            icon = folium.Icon(
                color="green", 
                icon="question", 
                prefix="fa"
            )
        ).add_to(no_name_fg)
    elif 'hill' in mountain['properties']['name'].lower():
        folium.Marker(
            location = [
                mountain["geometry"]["coordinates"][1],
                mountain["geometry"]["coordinates"][0]
            ],
            popup = mountain["properties"]["name"],
            icon = folium.Icon(
                color="blue", 
                icon="mound", 
                prefix="fa"
            )
        ).add_to(hills_fg)
    else:
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
hills_fg.add_to(m)
no_name_fg.add_to(m)

# Add sf borders
transit_map.add_sf_boundary(m)

# Add a layer control
folium.LayerControl().add_to(m)

m.save('local/mountains_map.html')
