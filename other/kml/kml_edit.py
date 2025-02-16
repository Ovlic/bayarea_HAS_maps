"""
import xml.etree.ElementTree as ET

trip_colors = {
  "1674275": 536930559,
  "1674399": 536930559,
  "1674537": 541636685,
  "1674655": 538617594,
  "1674881": 541636685,
  "1674977": 539237613,
  "1675157": 539237613,
  "1675337": 552578560,
  "1675455": 552578560,
  "1721165": 545433259,
  "1721350": 545433259
}

def parse_and_add_color(xml_file, output_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace handling (adjust if needed based on your XML)
    ns = {'ns': 'http://www.opengis.net/kml/2.2'}

    # Find all Placemark elements
    placemarks = root.findall('.//ns:Placemark', ns)

    for placemark in placemarks:
        # Generate or assign a color (example: assigning a fixed color)
        color = "539570163"  # Example color in ABGR format (red with full opacity)

        # Check if a <color> element already exists
        existing_color = placemark.find('ns:color', ns)
        if existing_color is None:
            # Create and append the <color> element
            color_element = ET.Element('color')
            color_element.text = color
            placemark.append(color_element)
        else:
            # Update the existing <color> element
            existing_color.text = color

    # Write back to the output file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

    print(f"Updated XML file saved as: {output_file}")

# Example usage
if __name__ == '__main__':
    input_file_path = 'caltrain.kml'  # Replace with your KML file path
    output_file_path = 'caltrain_new.kml'  # Replace with the desired output file path
    
    parse_and_add_color(input_file_path, output_file_path)
"""

"""import xml.etree.ElementTree as ET

# Dictionary mapping trip IDs to ABGR colors
trip_colors = {
    "1674275": 536930559,
    "1674399": 536930559,
    "1674537": 541636685,
    "1674655": 538617594,
    "1674881": 541636685,
    "1674977": 539237613,
    "1675157": 539237613,
    "1675337": 552578560,
    "1675455": 552578560,
    "1721165": 545433259,
    "1721350": 545433259
}

# Parse the KML file
file_path = "bart.kml"
tree = ET.parse(file_path)
root = tree.getroot()

# Define the namespace to handle the prefixed tags
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# Iterate through all Placemark elements
for placemark in root.findall(".//kml:Placemark", ns):
    # Extract the trip_id from the ExtendedData element
    extended_data = placemark.find(".//kml:ExtendedData", ns)
    if extended_data is not None:
        schema_data = extended_data.find(".//kml:SchemaData", ns)
        if schema_data is not None:
            simple_data = schema_data.find(".//kml:SimpleData[@name='trip_id']", ns)
            if simple_data is not None:
                trip_id = simple_data.text.strip()

                # Look up the color in the dictionary
                if trip_id in trip_colors:
                    # Get the corresponding color in ABGR format
                    color = trip_colors[trip_id]

                    # Convert the ABGR color to a KML-style hex color (AABBGGRR)
                    alpha = (color >> 24) & 0xFF
                    blue = (color >> 16) & 0xFF
                    green = (color >> 8) & 0xFF
                    red = color & 0xFF
                    kml_color = f"{alpha:02x}{blue:02x}{green:02x}{red:02x}"

                    # Update the color in the <LineStyle> element
                    line_style = placemark.find(".//kml:Style/kml:LineStyle", ns)
                    if line_style is not None:
                        color_elem = line_style.find("kml:color", ns)
                        if color_elem is not None:
                            color_elem.text = kml_color

# Save the modified KML back to a file
tree.write("bart_new.kml")
print("KML file has been modified with the new colors.")"""


import xml.etree.ElementTree as ET

# Parse the Caltrain KML file
file_path = "caltrain.kml"
tree = ET.parse(file_path)
root = tree.getroot()

# Define the namespace to handle the prefixed tags
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# Iterate through all Placemark elements
for placemark in root.findall(".//kml:Placemark", ns):
    # Create and add the <weight> tag to the Placemark
    weight = ET.Element("weight")
    weight.text = "5"
    placemark.append(weight)

# Save the modified KML back to a file
tree.write("caltrain_new.kml")
print("Caltrain KML file has been modified with the weight of 5.")

import xml.etree.ElementTree as ET

# Dictionary mapping trip IDs to ABGR colors
trip_colors = {
    "1674275": 536930559,
    "1674399": 536930559,
    "1674537": 541636685,
    "1674655": 538617594,
    "1674881": 541636685,
    "1674977": 539237613,
    "1675157": 539237613,
    "1675337": 552578560,
    "1675455": 552578560,
    "1721165": 545433259,
    "1721350": 545433259
}

# Parse the BART KML file
file_path = "bart.kml"
tree = ET.parse(file_path)
root = tree.getroot()

# Define the namespace to handle the prefixed tags
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# Iterate through all Placemark elements
for placemark in root.findall(".//kml:Placemark", ns):
    # Extract the trip_id from the ExtendedData element
    extended_data = placemark.find(".//kml:ExtendedData", ns)
    if extended_data is not None:
        schema_data = extended_data.find(".//kml:SchemaData", ns)
        if schema_data is not None:
            simple_data = schema_data.find(".//kml:SimpleData[@name='trip_id']", ns)
            if simple_data is not None:
                trip_id = simple_data.text.strip()

                # Look up the color in the dictionary
                if trip_id in trip_colors:
                    # Get the corresponding color in ABGR format
                    color = trip_colors[trip_id]

                    # Convert the ABGR color to a KML-style hex color (AABBGGRR)
                    alpha = (color >> 24) & 0xFF
                    blue = (color >> 16) & 0xFF
                    green = (color >> 8) & 0xFF
                    red = color & 0xFF
                    kml_color = f"{alpha:02x}{blue:02x}{green:02x}{red:02x}"

                    # Update the color in the <LineStyle> element
                    line_style = placemark.find(".//kml:Style/kml:LineStyle", ns)
                    if line_style is not None:
                        color_elem = line_style.find("kml:color", ns)
                        if color_elem is not None:
                            color_elem.text = kml_color

    # Add a <weight> tag with value 4
    weight = ET.Element("weight")
    weight.text = "4"
    placemark.append(weight)

# Save the modified KML back to a file
tree.write("bart_new.kml")
print("BART KML file has been modified with the weight of 4.")
