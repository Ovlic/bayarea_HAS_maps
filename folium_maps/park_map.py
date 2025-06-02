
# Load from data/tentacles_data/parks.geojson

import folium, json
import transit_map

print("before load data")
# Load the data
with open('data/tentacles_data/parks.geojson') as f:
    parks = json.load(f)

m = folium.Map(
    location=[37.7749, -122.4194], 
    zoom_start=12,
    tiles="cartodbpositron"
    )  # Default to San Francisco

print("before add_tiles")
transit_map.add_tiles(m)
print("after add_tiles")

# Print the tiles added to the map
print(m._children)
# Why are the other tiles not showing up?



# Add parks to map
folium.GeoJson(
    parks,
    name='Parks',
    tooltip=folium.GeoJsonTooltip(fields=['map_park_n']),
    # Add border (light blue) but make fill transparent
    style_function=lambda x: {
        'fillColor': 'transparent',
        # What color strings can be used here? 
        # https://www.w3schools.com/colors/colors_names.asp
        'color': '#40E0D0',
        'weight': 2
    },
    # Popup is the same as tooltip
    popup = folium.GeoJsonPopup(
        fields=['map_park_n'],
        aliases=['Park Name']
    )
).add_to(m)

# Add sf borders
transit_map.add_sf_boundary(m)

# Add a layer control
folium.LayerControl().add_to(m)

m.save('local/park_map.html')

# Add favicons
transit_map.add_favicons('local/park_map.html')