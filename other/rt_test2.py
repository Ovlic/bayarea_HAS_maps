from folium.plugins import Realtime
import folium
from folium import JsCode

# Initialize the map
m = folium.Map(location=[37.3778, -122.028389], zoom_start=12)

# Define Realtime layer with styled markers
rt = Realtime(
    "http://localhost:8000/vehicles.geojson",  # Ensure your GeoJSON file is served here
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
                <b>${lineRef}</b><br>
                Direction: <b>${vehicleRef}</b><br>
                Click for more info!
            `).bindTooltip('Im a vehicle!');
        }
    """),
    interval=10000,  # Fetch interval
)

# Add Realtime layer to the map
rt.add_to(m)

# Save to an HTML file
m.save("realtime_styled.html")
print("Map saved as 'realtime_styled.html'")
