
# Combine all the GEOJSONs within the folder called "districts" into one GEOJSON file called "districts.geojson"

import os
import json

# Create a list to store all the GEOJSONs
districts = []
districts_with_filenames = {}

file_paths = os.listdir("districts")
# Remove any directories
file_paths = [file for file in file_paths if os.path.isfile("districts/" + file)]
# Order the files in alphabetical order
file_paths.sort()
# Loop through all the files in the "districts" folder
for filename in file_paths:
    # Make sure its a file and not a folder
    if os.path.isfile("districts/" + filename):
        # Open the file
        with open("districts/" + filename, "r") as file:
            # Load the GEOJSON
            data = json.load(file)
            # Append the GEOJSON to the list
            districts.append(data)
            # Store the GEOJSON with the filename as the key
            districts_with_filenames[filename] = data


# TODO: Add these fields to the properties of the GEOJSON:
# - "District Number" (dist_no)
# - "Supervisor" (supervisor)
# - "ObjectID" (objectid)
# - "Shape Area" (shape_area)
# - "Shape Length" (shape_len)

district_property_fields = { # Dictionary of all the fields used for the properties of the district based on the file name
    "livermore.geojson": {
        "dist_no": "DIST_NAME", # Indicate that the district number must be split from the "NAME" field and that there will be information in the "split_by" field
        "split_by": "#", # Split the "NAME" field by a "#" to get the district number
        # There is no supervisor field in this file
        "dist_id": "DISTRICT_ID",
        "objectid": "OBJECTID",
        "shape_area": "Shape__Area",
        "shape_len": "Shape__Length"
    },
    "pleasanton.geojson": {
        "dist_no": "DIST_NAME",
        "split_by": "#",
        # There is no supervisor field in this file
        "dist_id": "DISTRICT_ID",
        "objectid": "OBJECTID",
        "shape_area": "Shape__Area",
        "shape_len": "Shape__Length"
    },
    "berkeley.geojson": {
        "dist_no": "DIST_NAME",
        "split_by": "#",
        "supervisor": "SUPERVISOR",
        "dist_id": "DISTRICT_ID",
        "objectid": "OBJECTID",
        "shape_area": "Shape__Area",
        "shape_len": "Shape__Length"
    },
    "san_jose.geojson": {
        "dist_no": "DISTRICTINT",
        "supervisor": "COUNCILMEMBER",
        # There is no dist_id field in this file
        "objectid": "OBJECTID",
        "shape_area": "SHAPE_Area",
        "shape_len": "SHAPE_Length",
        # Optional fields
        "population": "POPULATION",
        "housing_units": "HOUSING_UNITS",
    },
    "dublin.geojson": {
        "dist_no": "DIST_NAME",
        "split_by": "#",
        # There is no supervisor field in this file
        "dist_id": "DISTRICT_ID",
        "objectid": "OBJECTID",
        "shape_area": "Shape__Area",
        "shape_len": "Shape__Length"
    },
    "redwood_city.geojson": {
        "dist_no": "NAME",
        "split_by": "DISTRICT ",
        # There is no supervisor field in this file
        # There is no dist_id field in this file
        # There is no objectid field in this file
        "shape_area": "Shape_STAr",
        "shape_len": "Shape_STLe"
    },
    "san_leandro.geojson": {
        "dist_no": "DIST_NAME",
        "split_by": "#",
        # There is no supervisor field in this file
        "dist_id": "DISTRICT_ID",
        "objectid": "OBJECTID",
        "shape_area": "Shape__Area",
        "shape_len": "Shape__Length"
    },
    "san_francisco.geojson": {
        "dist_no": "sup_dist",
        "supervisor": "sup_name",
        # There is no dist_id field in this file
        # There is no objectid field in this file
        # There is no shape_area field in this file
        # There is no shape_len field in this file
    },
    "union_city.geojson": {
        "dist_no": "DIST_NAME",
        "split_by": "#",
        # There is no supervisor field in this file
        "dist_id": "DISTRICT_ID",
        "objectid": "OBJECTID",
        "shape_area": "Shape__Area",
        "shape_len": "Shape__Length"
    },
    "fremont.geojson": {
        "dist_no": "DIST_NAME",
        "split_by": "#",
        # There is no supervisor field in this file
        "dist_id": "DISTRICT_ID",
        "objectid": "OBJECTID",
        "shape_area": "Shape__Area",
        "shape_len": "Shape__Length"
    },
    "oakland.geojson": {
        "dist_no": "DIST_NAME",
        "split_by": "#",
        # There is no supervisor field in this file
        "dist_id": "DISTRICT_ID",
        "objectid": "OBJECTID",
        "shape_area": "Shape__Area",
        "shape_len": "Shape__Length"
    },
    "santa_clara.geojson": {
        "dist_no": "DISTRICTNO",
        # There is no supervisor field in this file
        # There is no dist_id field in this file
        "objectid": "OBJECTID",
        # There is no shape_area field in this file
        # There is no shape_len field in this file
    },
    "menlo_park.geojson": {
        "dist_no": "DISTRICT",
        "supervisor": "NAME",
        # There is no dist_id field in this file
        "objectid": "OBJECTID",
        "shape_area": "Shape__Are",
        "shape_len": "Shape__Len",
        # Optional fields
        "population": "POPULATION",
        "cvap": "TOTALCVAP",
    },
    "sunnyvale.geojson": {
        "dist_no": "DISTRICT",
        # There is no supervisor field in this file
        # There is no dist_id field in this file
        # There is no objectid field in this file
        # There is no shape_area field in this file
        # There is no shape_len field in this file
        # Optional fields
        "population": "POPULATION"
    },
    "hayward.geojson": {
        "dist_no": "fid",
        # There is no supervisor field in this file
        # There is no dist_id field in this file
        # There is no objectid field in this file
        # There is no shape_area field in this file
        # There is no shape_len field in this file
        # Optional fields
        "population": "POPULATION"
    },
    "south_san_francisco.geojson": {
        "dist_no": "DISTRICT",
        # There is no supervisor field in this file
        # There is no dist_id field in this file
        # There is no objectid field in this file
        "shape_area": "Shape__Area",
        "shape_len": "Shape__Length"
    },
    "stockton.geojson": {
        "dist_no": "district",
        "split_by": "DISTRICT ",
        "supervisor": "member",
        "split_by_sup": "Councilmember ",
        # There is no dist_id field in this file
        # There is no objectid field in this file
        # There is no shape_area field in this file
        # There is no shape_len field in this file
    },
    "concord.geojson": {
        "dist_no": "DISTRICT",
        "supervisor": "NAME",
        # There is no dist_id field in this file
        # There is no objectid field in this file
        "shape_area": "Shape_STAr",
        "shape_len": "Shape_STLe"
    },
    "antioch.geojson": {
        "dist_no": "ID",
        # There is no supervisor field in this file
        # There is no dist_id field in this file
        "objectid": "OBJECTID",
        "shape_area": "Shape_Area",
        "shape_len": "Shape_Length"
    },
}

# Loop through each feature and print the properties in the format "Key: Value"
for district, filename in zip(districts, districts_with_filenames):
    print(f"\n\nDistrict: {filename.split('.')[0].replace('_', ' ').title()}")
    if filename == "sunnyvale.geojson" or filename == "hayward.geojson" or filename == "south_san_francisco.geojson":
        # stupid amount of data in properties, i want to actually see the others so pls dont print
        print(" • (properties not printed)")
        continue
    for feature in district["features"]:
        for key, value in feature["properties"].items():
            print(f" • {key}: {value}")
        print()

district_geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Make a template for each feature
temp_feature = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": []
    },
    "properties": {
        "dist_no": "",
        "supervisor": "",
        "dist_id": "",
        "objectid": "",
        "shape_area": "",
        "shape_len": "" 
    }
}

for filename, data in districts_with_filenames.items():
    district_geojson["features"].extend(data["features"])
    cityname = filename.split('.')[0].replace('_', ' ').title()
    print(f"City: {cityname}")
    # This indent is for the city
    current_gj = {
        "type": "FeatureCollection",
        "features": []
    }
    for feature in data["features"]:
        properties = feature["properties"]
        # This indent is for the district
        prop_template = district_property_fields[filename]
        
        # dist_no
        # Check if the "split_by" field exists in the property template
        if "split_by" in prop_template:
            # Split the value by the split_by field
            dist_no = properties[prop_template["dist_no"]].split(prop_template["split_by"])[1]
        else:
            dist_no = properties[prop_template["dist_no"]]
    
        # supervisor
        # Check if "split_by_sup" exists in the property template
        if "split_by_sup" in prop_template:
            # Split the value by the split_by_sup field
            supervisor = properties[prop_template["supervisor"]].split(prop_template["split_by_sup"])[1]
        else:
            supervisor = getattr(prop_template, "supervisor", "")

        # dist_id
        if "dist_id" in prop_template:
            dist_id = properties[prop_template["dist_id"]]
        else:
            dist_id = ""

        # objectid
        if "objectid" in prop_template:
            objectid = properties[prop_template["objectid"]]
        else:
            objectid = ""

        # shape_area
        if "shape_area" in prop_template:
            shape_area = properties[prop_template["shape_area"]]
        else:
            shape_area = ""

        # shape_len
        if "shape_len" in prop_template:
            shape_len = properties[prop_template["shape_len"]]
        else:
            shape_len = ""

        # Add the properties to the current feature
        new_properties = {
            "dist_no": dist_no,
            "city": cityname,
            "supervisor": supervisor,
            "dist_id": dist_id,
            "objectid": objectid,
            "shape_area": shape_area,
            "shape_len": shape_len,
            "color": ""
        }
        # Add the properties to the current feature
        feature["properties"] = new_properties
        # Add the feature to the current GEOJSON
        current_gj["features"].append(feature)
    # Save to the directory "districts/new/"
    with open(f"districts/new/{filename}", "w") as file:
        # json.dump(current_gj, file)
        # Dump the file with proper indentation (tabs)
        json.dump(current_gj, file, indent=4)

                

# Write the combined GEOJSON to a file
with open("districts.geojson", "w") as file:
    json.dump(district_geojson, file)