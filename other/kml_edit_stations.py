import json
import xml.etree.ElementTree as ET

# Load the JSON data
with open('stations.json', 'r') as f:
    data = json.load(f)

# Create the KML root element and define the namespace
kml_ns = {"kml": "http://www.opengis.net/kml/2.2"}
kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
document = ET.SubElement(kml, "Document")

# Iterate through the operators and routes
for operator_id, operator_data in data.items():
    operator_folder = ET.SubElement(document, "Folder")
    operator_name = ET.SubElement(operator_folder, "name")
    operator_name.text = operator_id

    # Iterate through routes for each operator
    for route_id, route_data in operator_data.items():
        if route_id != "Contents":  # Skip "Contents" as it's not a route
            route_folder = ET.SubElement(operator_folder, "Folder")
            route_name = ET.SubElement(route_folder, "name")
            route_name.text = route_id

            # Iterate through stations for each route
            scheduled_stops = route_data.get("Contents", {}).get("dataObjects", {}).get("ScheduledStopPoint", [])
            for stop in scheduled_stops:
                station_name = stop.get("Name")
                latitude = stop.get("Location", {}).get("Latitude")
                longitude = stop.get("Location", {}).get("Longitude")
                url = stop.get("Url")

                if station_name and latitude and longitude:
                    placemark = ET.SubElement(route_folder, "Placemark")

                    # Station name
                    name = ET.SubElement(placemark, "name")
                    name.text = station_name

                    # Coordinates
                    coordinates = ET.SubElement(placemark, "Point")
                    coord_text = ET.SubElement(coordinates, "coordinates")
                    coord_text.text = f"{longitude},{latitude}"

                    # URL (optional)
                    if url:
                        extended_data = ET.SubElement(placemark, "ExtendedData")
                        schema_data = ET.SubElement(extended_data, "SchemaData")
                        schema_url = f"#{operator_id}_{route_id}"
                        schema_data.set("schemaUrl", schema_url)

                        simple_data = ET.SubElement(schema_data, "SimpleData", name="station_url")
                        simple_data.text = url

# Convert the KML structure to a string and save it to a file
tree = ET.ElementTree(kml)
tree.write("stations.kml", encoding="utf-8", xml_declaration=True)

print("KML file has been created successfully.")
