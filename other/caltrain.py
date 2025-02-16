import folium
import json

# Load the GeoJSON data
with open('filtered_muni_routes.geojson', 'r') as f:
    caltrain_geojson = json.load(f)

with open('colors.json', 'r') as f:
    colors = json.load(f)

# Create a Folium map centered around the approximate center of the line
m = folium.Map(location=[37.7117798, -122.4012505], zoom_start=12)

# Lambda for weight that makes Muni Metro lines thicker (weight=3) and Cable car and Historic streetcar lines thinner (weight=2)
weight_convert = lambda feature: 3 if feature['properties']['service_ca'] == "Muni Metro" else 2

# Add the GeoJSON layer
folium.GeoJson(
    data=caltrain_geojson,
    style_function=lambda feature: {
        # Get color from the colors.json file based on the lineabbr
        'color': colors["SF"][feature['properties']['lineabbr']],
        'weight': weight_convert(feature),
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['lineabbr', 'service_ca'],  # Tooltip fields from GeoJSON 'properties'
        aliases=['Name:', 'Type:'],  # Display aliases
    ),
).add_to(m)

# Save the map to an HTML file
m.save("caltrain_map.html")
print("Map saved to caltrain_map.html")
