"""import json
import xml.etree.ElementTree as ET

# Load the JSON data
with open('stations.json', 'r') as f:
    data = json.load(f)

# Create the KML root element and define the namespace
kml_ns = {"kml": "http://www.opengis.net/kml/2.2"}
kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
document = ET.SubElement(kml, "Document")

# Define a style for the placemarks (smaller icon and no label)
style = ET.SubElement(document, "Style", id="smallIconStyle")
icon_style = ET.SubElement(style, "IconStyle")
icon = ET.SubElement(icon_style, "Icon")
href = ET.SubElement(icon, "href")
href.text = "http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"  # Example icon URL
scale = ET.SubElement(icon_style, "scale")
scale.text = "0.5"  # Scale the icon to make it smaller (default is 1)

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

                    # Apply the style to the placemark
                    style_url = ET.SubElement(placemark, "styleUrl")
                    style_url.text = "#smallIconStyle"  # Reference the defined style

                    # Name (this will be used as a tooltip)
                    placemark_name = ET.SubElement(placemark, "name")
                    placemark_name.text = station_name  # Set the station name as the placemark's name

                    # Coordinates
                    coordinates = ET.SubElement(placemark, "Point")
                    coord_text = ET.SubElement(coordinates, "coordinates")
                    coord_text.text = f"{longitude},{latitude}"

                    # URL (optional)
                    if url:
                        extended_data = ET.SubElement(placemark, "ExtendedData")
                        simple_data = ET.SubElement(extended_data, "SimpleData", name="station_url")
                        simple_data.text = url

# Convert the KML structure to a string and save it to a file
tree = ET.ElementTree(kml)
tree.write("stations_test.kml", encoding="utf-8", xml_declaration=True)

print("KML file has been created successfully.")
""""""

import json
import xml.etree.ElementTree as ET

# Load the JSON data
with open('stations.json', 'r') as f:
    data = json.load(f)

# Create the KML root element and define the namespace
kml_ns = {"kml": "http://www.opengis.net/kml/2.2"}
kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
document = ET.SubElement(kml, "Document")

# Define a style for the placemarks (small icon and hidden label text)
style = ET.SubElement(document, "Style", id="smallIconStyle")
icon_style = ET.SubElement(style, "IconStyle")
icon = ET.SubElement(icon_style, "Icon")
href = ET.SubElement(icon, "href")
href.text = "http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"  # Example icon URL
scale = ET.SubElement(icon_style, "scale")
scale.text = "0.5"  # Scale the icon to make it smaller (default is 1)

# Hide the label text
label_style = ET.SubElement(style, "LabelStyle")
label_scale = ET.SubElement(label_style, "scale")
label_scale.text = "0"  # Hide the label text

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

                    # Apply the style to the placemark
                    style_url = ET.SubElement(placemark, "styleUrl")
                    style_url.text = "#smallIconStyle"  # Reference the defined style

                    # Name (this will be used as a tooltip)
                    placemark_name = ET.SubElement(placemark, "name")
                    placemark_name.text = station_name  # Set the station name as the placemark's name

                    # Coordinates
                    coordinates = ET.SubElement(placemark, "Point")
                    coord_text = ET.SubElement(coordinates, "coordinates")
                    coord_text.text = f"{longitude},{latitude}"

                    # URL (optional)
                    if url:
                        extended_data = ET.SubElement(placemark, "ExtendedData")
                        simple_data = ET.SubElement(extended_data, "SimpleData", name="station_url")
                        simple_data.text = url

# Convert the KML structure to a string and save it to a file
tree = ET.ElementTree(kml)
tree.write("stations_test2.kml", encoding="utf-8", xml_declaration=True)

print("KML file has been created successfully.")
"""

import json
import xml.etree.ElementTree as ET

# Load the JSON data
with open('train_bus/stations.json', 'r') as f:
    data = json.load(f)

# Create the KML root element and define the namespace
kml_ns = {"kml": "http://www.opengis.net/kml/2.2"}
kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
document = ET.SubElement(kml, "Document")

# Define a style for the placemarks (custom icon and hidden label text)
style = ET.SubElement(document, "Style", id="customCircleIconStyle")
icon_style = ET.SubElement(style, "IconStyle")
icon = ET.SubElement(icon_style, "Icon")
href = ET.SubElement(icon, "href")
href.text = "https://ovlic.com/bayarea_HAS_maps/station.png"  # Custom icon URL
scale = ET.SubElement(icon_style, "scale")
scale.text = "0.3"  # Scale the icon to make it smaller (default is 1)

# Hide the label text
label_style = ET.SubElement(style, "LabelStyle")
label_scale = ET.SubElement(label_style, "scale")
label_scale.text = "0"  # Hide the label text

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
            scheduled_stops = (
                route_data.get("Contents", {})
                .get("dataObjects", {})
                .get("ScheduledStopPoint", [])
            )
            for stop in scheduled_stops:
                station_name = stop.get("Name")
                latitude = stop.get("Location", {}).get("Latitude")
                longitude = stop.get("Location", {}).get("Longitude")
                url = stop.get("Url")
                if station_name and latitude and longitude:
                    placemark = ET.SubElement(route_folder, "Placemark")

                    # Apply the style to the placemark
                    style_url = ET.SubElement(placemark, "styleUrl")
                    style_url.text = "#customCircleIconStyle"  # Reference the defined style

                    # Name (this will be used as a tooltip)
                    placemark_name = ET.SubElement(placemark, "name")
                    placemark_name.text = station_name

                    # Description (clickable text content)
                    description = ET.SubElement(placemark, "description")
                    description.text = f"<b>Station:</b> {station_name}<br><b>URL:</b> {url or 'N/A'}"

                    # Coordinates
                    point = ET.SubElement(placemark, "Point")
                    coord_text = ET.SubElement(point, "coordinates")
                    coord_text.text = f"{longitude},{latitude}"

# Convert the KML structure to a string and save it to a file
tree = ET.ElementTree(kml)
tree.write("stations_with_bus.kml", encoding="utf-8", xml_declaration=True)
print("KML file has been created successfully.")

