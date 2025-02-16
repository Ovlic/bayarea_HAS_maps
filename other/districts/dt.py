"""
# Draw districts on a folium map from districts_colored.geojson
import folium, json, os

# Load multiple geojson files from the directory "districts/new/colored". Make sure to ignore anything that is not a geojson file.

# Load the GeoJSON data
geojsons = []
for file in os.listdir("districts/new/colored"):
    if file.endswith(".geojson"):
        with open(f"districts/new/colored/{file}") as f:
            geojsons.append(json.load(f))

# Use the "cartodbpositron" tiles
m = folium.Map(
    location=[37.7749, -122.4194],
    zoom_start=12,
    tiles="cartodbpositron"
)

# Loop through each feature in the GeoJSON data
for data in geojsons:
    for feature in data["features"]:
        # Get the district name
        name = feature["properties"]["dist_no"]
        color = feature["properties"]["color"]
        city = feature["properties"]["city"]
        
        the_tooltip = folium.GeoJsonTooltip(
            # Have both district number and city name in the tooltip
            fields=["dist_no", "city"],
            aliases=["District", "City"],
            localize=True
        )

        # Create a polygon for the district
        folium.GeoJson(
            feature,
            name=name,
            tooltip=the_tooltip,
            style_function=lambda x: {'fillColor': color}
        ).add_to(m)

# Save the map to an HTML file
m.save("districts_colored.html")"""

# Draw districts on a folium map from multiple GeoJSON files
import folium, json, os

# Load multiple geojson files from the directory "districts/new/colored"
geojsons = []
geojson_dir = "districts/new/colored/hopefully_this"

for file in os.listdir(geojson_dir):
    if file.endswith(".geojson"):
        file_path = os.path.join(geojson_dir, file)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                geojson_data = json.load(f)
                geojsons.append(geojson_data)
            except json.JSONDecodeError:
                print(f"Error loading {file}")

# Use the "cartodbpositron" tiles
m = folium.Map(
    location=[37.7749, -122.4194],
    zoom_start=12,
    tiles="cartodbpositron"
)

# Function to ensure the geometry is either Polygon or MultiPolygon
def clean_geometry(feature):
    geometry = feature["geometry"]
    if geometry["type"] == "GeometryCollection":
        # Extract the first valid MultiPolygon or Polygon
        polygons = [g for g in geometry["geometries"] if g["type"] in ["Polygon", "MultiPolygon"]]
        if polygons:
            feature["geometry"] = polygons[0]  # Replace with the first valid geometry
    return feature

# Loop through each feature in the GeoJSON data
for data in geojsons:
    for feature in data["features"]:
        feature = clean_geometry(feature)  # Fix GeometryCollection issue
        
        # Get the district name, city, and color
        name = feature["properties"].get("dist_no", "Unknown District")
        city = feature["properties"].get("city", "Unknown City")
        color = feature["properties"].get("fill", "#3388ff")  # Default color
        
        the_tooltip = folium.GeoJsonTooltip(
            fields=["dist_no", "city"],
            aliases=["District", "City"],
            localize=True
        )

        # Create a polygon for the district
        folium.GeoJson(
            feature,
            name=f"{city} - District {name}",
            tooltip=the_tooltip,
            style_function=lambda x, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.6  # Ensures visibility
            }
        ).add_to(m)

# Save the map to an HTML file
m.save("districts_colored.html")
print("Map saved as districts_colored.html")
