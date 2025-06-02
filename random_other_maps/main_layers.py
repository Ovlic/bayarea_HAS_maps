import json
import math
from shapely.geometry import Polygon, mapping
from shapely.ops import unary_union
import folium
from utils import makeBeautifyIcon

# Constants
radius_meters = 402.336  # Radius for station circles in meters
earth_radius = 6378137  # Earth's radius in meters
map_bounds = [[-123.0, 36.5], [-121.0, 39.0]]  # Map bounds (SW and NE corners)
operators = ['CE', 'BA', 'CT', 'AM', 'SI', 'SF', 'SA', 'SC']  # Transit operators

# Create map
m = folium.Map(
    location=[37.65077186632317, -122.24094250022335],
    zoom_start=9,
    tiles="cartodbpositron"
)

# Load data
with open('rail_lines.json', 'r') as f:
    rail_lines = json.load(f)
with open('stations.json', 'r') as f:
    stations = json.load(f)
with open('colors.json', 'r') as f:
    colors = json.load(f)
with open('shapes.json', 'r') as f:
    shapes = json.load(f)
with open('route_trip_ids.json', 'r') as f:
    route_trip_ids = json.load(f)

# Helper functions
def create_circle(lat, lon, radius_meters, resolution=72):
    " ""Create a circular polygon around a point." ""
    lat_radius = radius_meters / earth_radius * (180 / math.pi)
    lon_radius = radius_meters / (earth_radius * math.cos(math.radians(lat))) * (180 / math.pi)
    points = [
        (
            lon + lon_radius * math.cos(math.radians(angle)),
            lat + lat_radius * math.sin(math.radians(angle))
        )
        for angle in range(0, 360, int(360 / resolution))
    ]
    return Polygon(points)

# Create the outer polygon for the shaded area
outer_polygon = Polygon([
    (map_bounds[0][0], map_bounds[0][1]),  # SW
    (map_bounds[1][0], map_bounds[0][1]),  # NW
    (map_bounds[1][0], map_bounds[1][1]),  # NE
    (map_bounds[0][0], map_bounds[1][1]),  # SE
    (map_bounds[0][0], map_bounds[0][1])   # Back to SW
])

# Create the map and other initial setup (unchanged)

# Create the map and other initial setup (unchanged)

# Assign the map object to `window.map` for global access
m.get_root().html.add_child(folium.Element("""
<script>
    // Ensure map object is correctly accessible
    window.map = L.map('map');
</script>
"""))

# Add layers and features (unchanged)
circle_shapes = []
line_layers = {}
for operator in operators:
    if operator not in stations or operator not in shapes:
        continue

    for line_id, line_stations in stations[operator].items():
        layer = folium.FeatureGroup(name=f"{operator} {line_id}")

        # Add train line (unchanged)
        if line_id in shapes[operator]:
            coords = [(lat, lon) for lon, lat in shapes[operator][line_id]]
            color = route_trip_ids[operator].get(line_id, {}).get('color', 'blue')
            folium.PolyLine(coords, color=color, weight=3).add_to(layer)

        # Add stations and their circles
        for stop in line_stations["Contents"]["dataObjects"]["ScheduledStopPoint"]:
            lat, lon = float(stop["Location"]["Latitude"]), float(stop["Location"]["Longitude"])

            # Add station marker (unchanged)
            folium.Marker(
                location=[lat, lon],
                popup=stop['Name'],
                icon=makeBeautifyIcon(
                    icon=None,
                    border_color="#000000",
                    border_width=3,
                    text_color="#b3334f",
                    icon_shape="circle",
                    inner_icon_style="opacity: 0;",
                    icon_size=[13, 13],
                )
            ).add_to(layer)

            # Add circle and trigger shaded area update
            circle = create_circle(lat, lon, radius_meters)
            circle_shapes.append(circle)

            # Add the circle to the map dynamically
            folium.CircleMarker([lat, lon], radius=5).add_to(layer)

        line_layers[line_id] = layer
        m.add_child(layer)

# Generate initial shaded area (unchanged)
merged_circles = unary_union(circle_shapes)
shaded_area = outer_polygon.difference(merged_circles)
shaded_geojson = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "geometry": mapping(shaded_area),
        "properties": {
            "fill": "#000000",
            "fill-opacity": 0.6,
            "stroke": False,
        },
    }]
}

# Add shaded area to map (unchanged)
shaded_layer = folium.FeatureGroup(name="Shaded Area")
folium.GeoJson(
    shaded_geojson,
    style_function=lambda x: {
        'fillColor': x['properties']['fill'],
        'fillOpacity': x['properties']['fill-opacity'],
        'color': 'none'
    }
).add_to(shaded_layer)
m.add_child(shaded_layer)

# Add LayerControl for toggling (unchanged)
folium.LayerControl().add_to(m)

# Add the script for dynamic shaded area update earlier in the document
update_script = """
function updateShadedArea() {
    const outerPolygon = turf.polygon([
        [
            [-123.0, 36.5], [-121.0, 36.5], 
            [-121.0, 39.0], [-123.0, 39.0], 
            [-123.0, 36.5]  // Coordinates of your map bounds
        ]
    ]);

    const layers = [];
    window.map.eachLayer(function(layer) {
        if (layer instanceof L.Circle) {
            const latLng = layer.getLatLng();
            const radius = layer.getRadius();
            const circleGeoJson = turf.circle([latLng.lng, latLng.lat], radius, {steps: 72, units: 'meters'});
            layers.push(circleGeoJson);
        }
    });

    const combinedCircles = turf.featureCollection(layers);
    const union = turf.union(...combinedCircles.features);
    const shaded = turf.difference(outerPolygon, union);
    
    // Clear previous shaded area
    if (window.shadedLayer) {
        window.map.removeLayer(window.shadedLayer);
    }

    // Add new shaded area
    window.shadedLayer = L.geoJSON(shaded, {
        style: {fillColor: '#000', fillOpacity: 0.6, color: 'none'}
    }).addTo(window.map);
}

// Delay the call to `updateShadedArea` to ensure map is fully initialized
setTimeout(updateShadedArea, 1000);
"""

# Ensure the updateShadedArea function is loaded in the HTML before being called
m.get_root().html.add_child(folium.Element(f"<script>{update_script}</script>"))

# Save the map (unchanged)
m.save('map_with_layers.html')
