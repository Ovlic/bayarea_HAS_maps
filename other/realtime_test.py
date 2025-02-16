
import folium
from folium import JsCode
from folium.plugins import Realtime
import requests
import json
import threading
import time
import os
import dotenv

# Load the .env file
dotenv.load_dotenv()

key = os.getenv('API_511')

# Function to transform API data to GeoJSON
def convert_to_geojson(api_data):
    activities = api_data.get("geometry", {}).get("Siri", {}).get("ServiceDelivery", {}).get("VehicleMonitoringDelivery", {}).get("VehicleActivity", [])
    features = []
    for activity in activities:
        journey = activity.get("MonitoredVehicleJourney", {})
        location = journey.get("VehicleLocation", {})
        vehicle_ref = journey.get("VehicleRef", "Unknown")
        line_ref = journey.get("LineRef", "Unknown")
        destination = journey.get("DestinationName", "Unknown")
        latitude = location.get("Latitude")
        longitude = location.get("Longitude")

        if latitude and longitude:
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [float(longitude), float(latitude)]},
                "properties": {"VehicleRef": vehicle_ref, "LineRef": line_ref, "DestinationName": destination}
            })
    return {"type": "FeatureCollection", "features": features}

# Function to fetch and transform API data into GeoJSON format
def fetch_and_save_geojson(api_url, output_file):
    while True:
        response = requests.get(api_url)
        data = response.json()

        # Transform API response to GeoJSON format
        geojson_data = convert_to_geojson(data)

        # Save to file
        with open(output_file, "w") as f:
            json.dump(geojson_data, f)

        print(f"GeoJSON data saved to {output_file}")
        time.sleep(10)  # Fetch interval (match Realtime `interval`)

# API URL
api_url = f"https://api.511.org/transit/VehicleMonitoring?agency=CT&api_key={key}"
output_file = "vehicles.geojson"

# Start the data-fetching thread
threading.Thread(target=fetch_and_save_geojson, args=(api_url, output_file), daemon=True).start()

# Create the map
m = folium.Map(location=[37.3778, -122.028389], zoom_start=12)

# Add Realtime layer using the local GeoJSON file
rt = Realtime(
    output_file,
    interval=10000,
    get_feature_id=JsCode("(f) => {return f.properties.VehicleRef;}"),
    point_to_layer=JsCode("""
        (f, latlng) => {
            // Extract properties for customization
            const borderColor = f.properties.icon_color || '#DD1F29'; // Default color
            const textColor = f.properties.text_color || '#b3334f';   // Default text color
            const vehicleRef = f.properties.VehicleRef || 'N/A';
            const lineRef = f.properties.LineRef || 'Unknown';

            // Create a styled icon using Leaflet divIcon
            const iconHtml = `
                <div style="
                    background-color: white;
                    border: 2px solid ${borderColor};
                    border-radius: 50%;
                    width: 30px;  /* Adjusted size */
                    height: 30px; /* Adjusted size */
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: ${textColor};
                    font-size: 12px; /* Smaller font for the icon */
                    font-weight: bold;
                    padding: 0;  /* Remove extra space */
                ">
                    <i class="fa fa-train"></i>
                </div>
            `;

            // Return a marker with the styled icon
            return L.marker(latlng, {
                icon: L.divIcon({
                    html: iconHtml,
                    className: 'custom-icon',
                    iconSize: [30, 30], // Adjusted size of the icon
                    popupAnchor: [0, -15], // Adjusted popup position
                })
            }).bindPopup(`
                <b>${lineRef} ${vehicleRef}</b><br>
                Direction: <b>${vehicleRef % 2 == 0 ? 'South' : 'North'}</b><br>
                Click for more info!
            `).bindTooltip('Im a vehicle!');
        }
    """),
)
rt.add_to(m)

# Add realtime for SF (File: vehicles_sf.geojson)
# Get the color to use for the icon from colors.json

with open("colors.json", "r") as f:
    colors = json.load(f)

sf_colors = colors["SF"]

rt_sf = Realtime(
    "vehicles_sf.geojson",
    interval=10000,
    get_feature_id=JsCode("(f) => {return f.properties.VehicleRef;}"),
    point_to_layer=JsCode("""
        (f, latlng) => {
            // Extract properties for customization
            const borderColor = f.properties.icon_color || '#1E90FF'; // Default color
            const textColor = f.properties.icon_color || '#1E90FF';   // Default text color 
            const vehicleRef = f.properties.VehicleRef || 'N/A';
            const lineRef = f.properties.LineRef || 'Unknown';

            // Create a styled icon using Leaflet divIcon
            const iconHtml = `
                <div style="
                    background-color: white;
                    border: 2px solid ${borderColor};
                    border-radius: 50%;
                    width: 30px;  /* Adjusted size */
                    height: 30px; /* Adjusted size */
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: ${textColor};
                    font-size: 12px; /* Smaller font for the icon */
                    font-weight: bold;
                    padding: 0;  /* Remove extra space */
                ">
                    <i class="fa fa-train"></i>
                </div>
            `;

            // Return a marker with the styled icon
            return L.marker(latlng, {
                icon: L.divIcon({
                    html: iconHtml,
                    className: 'custom-icon',
                    iconSize: [30, 30], // Adjusted size of the icon
                    popupAnchor: [0, -15], // Adjusted popup position
                })
            }).bindPopup(`
                <b>${lineRef} ${vehicleRef}</b><br>
                Direction: <b>${vehicleRef % 2 == 0 ? 'South' : 'North'}</b><br>
                Click for more info!
            `).bindTooltip('Im a vehicle!');
        }
    """),
)
rt_sf.add_to(m)




# Save the map
m.save("realtime.html")
print("Map saved to realtime.html!")
