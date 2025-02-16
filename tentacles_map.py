
import folium, json, os, dotenv
from location_test import add_location_circle
from folium.plugins import LocateControl
from xyzservices import TileProvider
import transit_map

# Load .env file
dotenv.load_dotenv()

folder_path = "tentacles_data"
with open(os.path.join(folder_path, "hospitals.geojson"), "r") as f:
    hospitals = json.load(f)

with open(os.path.join(folder_path, "libraries.geojson"), "r") as f:
    libraries = json.load(f)

with open(os.path.join(folder_path, "movie_theaters.geojson"), "r") as f:
    movie_theaters = json.load(f)

with open(os.path.join(folder_path, "museums.geojson"), "r") as f:
    museums = json.load(f)

with open(os.path.join(folder_path, "zoos.geojson"), "r") as f:
    zoos = json.load(f)

# Load San Francisco County boundary GeoJSON
with open('sf.geojson', 'r') as f:
    sf_boundary_geojson = json.load(f)

# Create the folium map
m = folium.Map(
    location=[37.7749, -122.4194], 
    zoom_start=12,
    tiles="cartodbpositron"
    )  # Default to San Francisco

# Add tile options
# OpenStreetMap
folium.TileLayer('openstreetmap', show=False).add_to(m)
# CartoDB Voyager
folium.TileLayer('cartodbvoyager', show=False).add_to(m)
# CartoDB Dark Matter
folium.TileLayer('cartodbdark_matter', show=False).add_to(m)
# Esri World Imagery
folium.TileLayer('esriworldimagery', show=False).add_to(m)
# JAWG Dark
# API Key for JAWG: ESd8imo0KmtipTKSQYSSN2Tvnu2LljJPeTnVaqVXRf84Zt378nCGRPhsqxIosl88
jdark = TileProvider(
    name="JAWG Dark",
    url="https://tile.jawg.io/jawg-dark/{z}/{x}/{y}.png?api-key="+os.getenv("JAWG_KEY"),
    attribution="JAWG Dark",
    accessToken="ESd8imo0KmtipTKSQYSSN2Tvnu2LljJPeTnVaqVXRf84Zt378nCGRPhsqxIosl88",
)

folium.TileLayer(jdark, show=False).add_to(m)

# Add lines and stops to map
transit_map.add_stations(m)
transit_map.add_lines(m)


# FeatureGroups
hospitals_fg = folium.FeatureGroup(name="Hospitals")
libraries_fg = folium.FeatureGroup(name="Libraries")
movie_theaters_fg = folium.FeatureGroup(name="Movie Theaters")
museums_fg = folium.FeatureGroup(name="Museums")
zoos_fg = folium.FeatureGroup(name="Zoos")


# Loop through each feature in the GeoJSON files
for feature in hospitals["features"]:
    lat = feature["geometry"]["coordinates"][1]
    lon = feature["geometry"]["coordinates"][0]
    folium.Marker(
        location=[lat, lon],
        popup=feature["properties"]["Name"],
        icon=folium.Icon(color="red", icon="plus")
    ).add_to(hospitals_fg)

for feature in libraries["features"]:
    lat = feature["geometry"]["coordinates"][1]
    lon = feature["geometry"]["coordinates"][0]
    folium.Marker(
        location=[lat, lon],
        popup=feature["properties"]["Name"],
        icon=folium.Icon(color="green", icon="book")
    ).add_to(libraries_fg)

for feature in movie_theaters["features"]:
    lat = feature["geometry"]["coordinates"][1]
    lon = feature["geometry"]["coordinates"][0]
    folium.Marker(
        location=[lat, lon],
        popup=feature["properties"]["Name"],
        icon=folium.Icon(color="blue", icon="film")
    ).add_to(movie_theaters_fg)

for feature in museums["features"]:
    lat = feature["geometry"]["coordinates"][1]
    lon = feature["geometry"]["coordinates"][0]
    folium.Marker(
        location=[lat, lon],
        popup=feature["properties"]["Name"],
        icon=folium.Icon(color="purple", icon="info-sign")
    ).add_to(museums_fg)

for feature in zoos["features"]:
    lat = feature["geometry"]["coordinates"][1]
    lon = feature["geometry"]["coordinates"][0]
    folium.Marker(
        location=[lat, lon],
        popup=feature["properties"]["Name"],
        icon=folium.Icon(color="orange", icon="leaf")
    ).add_to(zoos_fg)

# Add FeatureGroups to the map
hospitals_fg.add_to(m)
libraries_fg.add_to(m)
movie_theaters_fg.add_to(m)
museums_fg.add_to(m)
zoos_fg.add_to(m)

# Add San Francisco County boundary to the map
# Add the boundary to the map
folium.GeoJson(
    sf_boundary_geojson,
    style_function=lambda feature: {
        'color': '#FF0000',   # Red boundary line
        # No inner fill
        'fillOpacity': 0,
        'weight': 5,          # Line thickness
    },
    name="San Francisco County Boundary",
).add_to(m)

# Add Location HTML
# add_location_circle(m, 1609.34) # 1 mile in meters

# Add plugins
transit_map.add_plugins(m, location_circle=True, radius_meters=1609.34)

# Save the map
m.save("tentacles_map.html")