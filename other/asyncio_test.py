import asyncio
import aiohttp
import json
import os
import dotenv

dotenv.load_dotenv()
key = os.getenv('API_511')

with open('colors.json', 'r') as f:
    colors = json.load(f)
colors_sf = colors["SF"]
# Async function to fetch data from the API
async def fetch_data(url):
    # url = "https://api.511.org/transit/VehicleMonitoring?agency=CT&api_key=key"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data_raw = await response.text()
                data = json.loads(data_raw.encode().decode('utf-8-sig'))
                return data
            else:
                print(f"Error: {response.status}")
                return None

# Function to filter and format SF data
def format_sf_data(data):
    # Only keep the data that has "PH", "CA", "F", "J", "K", "L", "M", "N", "T", "PM" in LineRef
    data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]["VehicleActivity"] = [activity for activity in data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]["VehicleActivity"] if activity["MonitoredVehicleJourney"]["LineRef"] in ["PH", "CA", "F", "J", "K", "L", "M", "N", "T", "PM"]]
    # Add line color based on LineRef and colors.json
    for activity in data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]["VehicleActivity"]:
        activity["MonitoredVehicleJourney"]["icon_color"] = colors_sf.get(activity["MonitoredVehicleJourney"]["LineRef"], "#000000")
    # print(data)
    return data

# Async function to save data to GeoJSON file
async def save_geojson(data, filename):
    if data:
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(activity["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]),
                            float(activity["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]),
                        ],
                    },
                    "properties": {
                        "VehicleRef": activity["MonitoredVehicleJourney"]["VehicleRef"],
                        "LineRef": activity["MonitoredVehicleJourney"]["LineRef"],
                        # If icon_color is not in the data, don't include it in the properties
                        "icon_color": activity["MonitoredVehicleJourney"].get("icon_color"),
                    },
                }
                for activity in data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"]["VehicleActivity"]
            ],
        }
        with open(filename, "w") as file:
            json.dump(geojson_data, file)
        print(f"{filename} updated.")

# Periodic task to fetch and save data
async def periodic_task(interval):
    while True:
        print("Fetching and updating GeoJSON data...")
        data = await fetch_data(f"https://api.511.org/transit/VehicleMonitoring?agency=CT&api_key={key}")
        await save_geojson(data, "vehicles.geojson")

        data2 = await fetch_data(f"https://api.511.org/transit/VehicleMonitoring?agency=SF&api_key={key}")
        data2 = format_sf_data(data2)
        await save_geojson(data2, "vehicles_sf.geojson")
        await asyncio.sleep(interval)

# Main entry point for asyncio
async def main():
    # Run the periodic task every 10 seconds
    await periodic_task(30)

# Start the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
