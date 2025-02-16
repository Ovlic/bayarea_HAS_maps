import folium
import math

def generate_circle_coords(center, radius, n_points=72):
    """
    Generate coordinates for a circle around a given center.
    :param center: Tuple of (latitude, longitude)
    :param radius: Radius of the circle in meters
    :param n_points: Number of points to generate for the circle
    :return: List of (longitude, latitude) tuples
    """
    lat, lon = center
    earth_radius = 6378137  # Earth's radius in meters
    circle_coords = []

    for i in range(n_points):
        angle = math.radians(float(i) / n_points * 360)
        d_lat = (radius / earth_radius) * math.cos(angle)
        d_lon = (radius / earth_radius) * math.sin(angle) / math.cos(math.radians(lat))
        circle_coords.append((lon + math.degrees(d_lon), lat + math.degrees(d_lat)))

    return circle_coords

# Define the map
m = folium.Map(
    location=[37.65077186632317, -122.24094250022335],
    zoom_start=9,
)

# Generate coordinates for the outer and inner circles
outer_circle = generate_circle_coords(
    center=(37.65077186632317, -122.24094250022335), radius=5000
)
inner_circle = generate_circle_coords(
    center=(37.65077186632317, -122.24094250022335), radius=2500
)[::-1]  # Reverse the inner circle for GeoJSON hole

# Combine the coordinates into a single polygon with a hole
donut_coords = [outer_circle + inner_circle]

# Create a GeoJSON object for the donut
donut_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": donut_coords,
            },
            "properties": {
                "fill": "#3186cc",
                "fill-opacity": 0.5,
                "stroke": False,
            },
        }
    ],
}

# Add the donut shape to the map
folium.GeoJson(
    donut_geojson,
    style_function=lambda x: {
        'fillColor': x['properties']['fill'],
        'fillOpacity': x['properties']['fill-opacity'],
        'color': 'none'
    }
).add_to(m)

# Save the map to an HTML file
m.save('circle.html')
