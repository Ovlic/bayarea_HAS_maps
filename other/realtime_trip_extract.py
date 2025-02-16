
# Get a dictionary of all the trip ids found in route_trip_ids.json with the trip id as the key and the hex color passed in to the function convert_hex_string imported from color_convert.py as the value.

# The hex color should be converted to an integer using the convert_hex_string function before being stored in the dictionary.

# Example of data found in route_trip_ids.json:
"""
"CE" (operator id): {
        "ACETrain" (route name): {
            "trip_ids" ( the ids we want): [],
            "shape" (the shape of the route): []
            "color" (the color we want): "#9c67a0"
        }
    }
"""

import json
from color_convert import convert_hex_string

# Load the route_trip_ids.json file
with open('route_trip_ids.json') as f:
    route_trip_ids = json.load(f)

# Initialize an empty dictionary to store the trip ids and colors
trip_colors = {}

# Iterate through the operators and routes
for operator_id, operator_data in route_trip_ids.items():
    for route_id, route_data in operator_data.items():
        # Get the color for the route
        color = route_data.get("color")
        if color:
            # Convert the hex color to an integer
            color_int = convert_hex_string(color)
            # Iterate through the trip ids
            trip_ids = route_data.get("trip_ids")
            for trip_id in trip_ids:
                # Store the trip id and color in the dictionary
                trip_colors[trip_id] = color_int


# pretty print the dictionary
print(json.dumps(trip_colors, indent=4))