import folium, json
from pprint import pprint

import transit_map
from location_test import (
    add_location_circle2 as add_location_circle,
    add_location_circles2 as add_location_circles,
)
from folium.plugins import LocateControl
from folium import Element
from folium.map import Layer

from branca.element import Template, MacroElement

# Load radar_script.js
with open("radar_script.js", "r") as f:
    radar_js = f.read()

# Create a map centered at San Francisco
m = folium.Map(location=[37.7749, -122.4194], zoom_start=12, tiles="cartodbpositron")

# Add other tile layers
transit_map.add_tiles(m)

# Add stations
transit_map.add_stations(m, test=True)

# Add lines
transit_map.add_lines2(m)

# Add the SF boundary
transit_map.add_sf_boundary(m)

"""
for(var key in map._layers){
    let layer = map._layers[key]
    if("_layers" in layer){
        console.log("-----"+i.toString()+"------");
        console.log(Object.keys(layer._layers).length);
    }
}
"""

# Print map layers
# print(m._children)
# layers = {}
# for name, layer in m._children.items():
#     try:
#         if isinstance(layer, (folium.FeatureGroup, folium.TileLayer)):
#             thename = layer.tile_name
#         elif isinstance(layer, folium.PolyLine):
#             thename = layer._name
#         elif isinstance(layer, Layer):
#             thename = layer.layer_name
#         else:
#             thename = layer.name
#         # print([_name for _name, d in layer._children.items()])
#         layers[thename] = layer
#     except AttributeError:
#         print(f"This layer does not have a name attribute")
#         print(layer)
# print("After loop")
# pprint(layers)

# # Add a string as an id for each layer (its just the key with no spaces)
# for name, layer in layers.items():
#     layer.layer_name = name.replace(" ", "")

# Add custom location control


def OLD_add_location_circle(m, radius):
    # Create a FeatureGroup in Python for the circle
    location_layer = folium.FeatureGroup(name="Location Radius").add_to(m)

    # JavaScript to store the Python-generated FeatureGroup as a global variable
    js = f"""
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        var map = document.querySelector(".folium-map")._leaflet_map;

        // Assign the "Location Radius" layer to a global variable
        window.locationLayer = null;
        map.eachLayer(function(layer) {{
            if (layer.options && layer.options.name === "Location Radius") {{
                window.locationLayer = layer;
            }}
        }});

        if (!window.locationLayer) {{
            console.error("Location Radius layer not found");
            return;
        }}

        function updateCircle(e) {{
            window.locationLayer.clearLayers();  // Remove old circles
            // Add a popup with the radius in miles
        
            L.circle(e.latlng, {{
                radius: {radius},  
                color: 'blue',
                // fillColor: 'blue',
                // fillOpacity: 0.2
            }}).addTo(window.locationLayer);
        }}

        map.on("locationfound", updateCircle);
    }});
    </script>
    """

    map_find_html = """
    <script>
    L.Map.addInitHook(function () {
        this.getContainer()._leaflet_map = this;
    });
    </script>
    """

    # Inject JavaScript into the map
    m.get_root().html.add_child(Element(map_find_html))
    m.get_root().html.add_child(Element(js))

    return location_layer  # Return the FeatureGroup for LayerControl


# Distances (miles): 1/4, 1/2, 1, 3, 5, 7

# Add LocateControl
LocateControl(
    # auto_start=True
).add_to(m)

# Add all location circles
add_location_circles(m, [402.336, 804.672, 1609.34, 4828.03, 8046.72, 11265.4])
# # 7 Miles
# add_location_circle(m, 11265.4, "7 Miles", 6)

# # 5 Miles
# add_location_circle(m, 8046.72, "5 Miles", 5)
# # 3 miles
# add_location_circle(m, 4828.03, "3 Miles", 4)
# # 1 mile
# add_location_circle(m, 1609.34, "1 Mile", 3)
# # 1/2 mile
# add_location_circle(m, 804.672, "1/2 Miles", 2)
# # 1/4 mile
# add_location_circle(m, 402.336, "1/4 Miles", 1)

# # Add the location circle (1/4 mile radius)
# add_location_circle(m, 402.336, "1/4 Miles", 1)
# # 1/2 mile
# add_location_circle(m, 804.672, "1/2 Miles", 2)
# # 1 mile
# add_location_circle(m, 1609.34, "1 Mile", 3)
# # 3 miles
# add_location_circle(m, 4828.03, "3 Miles", 4)
# # 5 miles
# add_location_circle(m, 8046.72, "5 Miles", 5)
# # 7 miles
# add_location_circle(m, 11265.4, "7 Miles", 6)


# Add custom text
# Injecting custom css through branca macro elements and template, give it a name
textbox_css = """
{% macro html(this, kwargs) %}
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
  </head>

    <body>
        <div id="textbox" class="textbox">
            <div class="textbox-header">
                <div class="textbox-title">Note</div>
                <button id="close-textbox" class="close-button">&times;</button>
            </div>
            <div class="textbox-content">
                <p>I threw this up together relatively quickly and have not had the chance to test its accuracy. I will eventually have time to test it and tweak settings but for now it may be slightly inaccurate (but does it really matter on such a big scale? Probably not).</p>
                <p>Also, I want to add adjustable distances and a way to toggle the circles on and off, but I have not found a way to do that yet.</p>
            </div>
        </div>

        <script>
            document.addEventListener("DOMContentLoaded", function() {
                document.getElementById("close-textbox").addEventListener("click", function() {
                document.getElementById("textbox").style.display = "none";
                });
            });
            </script>

    </body>
</html>

<style type='text/css'>
  .textbox {
    position: absolute;
    z-index:9999;
    border-radius:4px;
    background: rgba( 28, 25, 56, 0.25 );
    box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.37 );
    backdrop-filter: blur( 4px );
    -webkit-backdrop-filter: blur( 4px );
    border: 4px solid rgba( 215, 164, 93, 0.2 );
    padding: 10px;
    font-size:14px;
    right: 20px;
    bottom: 20px;
    color: purple;
  }
  .textbox-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .textbox .textbox-title {
    color: darkpurple;
    text-align: center;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 22px;
  }
  .close-button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: purple;
  }
  .close-button:hover {
    color: red;
  }
</style>
{% endmacro %}
"""
# configuring the custom style (you can call it whatever you want)
my_custom_style = MacroElement()
my_custom_style._template = Template(textbox_css)

# Adding my_custom_style to the map
m.get_root().add_child(my_custom_style)

# Add custom layer control to map
layer_control_js = f"""
    <script src="static/L.Control.Layers.Tree.js"></script>
    <link rel="stylesheet" href="static/L.Control.Layers.Tree.css">

    <script>
    {radar_js}
    </script>
"""

m.get_root().html.add_child(Element(layer_control_js))

# Add plugins
# transit_map.add_plugins(m)

# Save the map
m.save("local/radarNew.html")

# Add favicons
# transit_map.add_favicons("local/radarNew.html")
