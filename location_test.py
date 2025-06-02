
from folium import Element

# Add multiple location circles
'''def add_location_circles(m, radii):
    # JavaScript to update multiple circles dynamically
    js = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        var map = document.querySelector(".folium-map")._leaflet_map;

        if (!window.userCircles) {{
            window.userCircles = [];
        }}

        function updateCircles(e) {{
            let radii = {radii};  // List of radii in meters
            radii.forEach((radius, index) => {{
                if (window.userCircles[index]) {{
                    window.userCircles[index].setLatLng(e.latlng);
                }} else {{
                    window.userCircles[index] = L.circle(e.latlng, {{
                        radius: radius,
                        color: 'black',
                        fillColor: 'blue',
                        fillOpacity: 0.2
                    }}).addTo(map);
                    window.userCircles[index].bindPopup("Radius: " + radius + " meters");
                }}
            }});
        }}

        map.on("locationfound", updateCircles);
    }});
    </script>
    """.format(radii=radii)

    map_find_html = """
    <script>
    L.Map.addInitHook(function () {
        this.getContainer()._leaflet_map = this;
    });
    </script>
    """

    # Add the map_find_html to the map
    m.get_root().html.add_child(Element(map_find_html))
    # Add the JS script to the map
    m.get_root().html.add_child(Element(js))'''
'''def add_location_circles(m, radii):
    # JavaScript to update multiple circles dynamically with layer control
    js = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        var map = document.querySelector(".folium-map")._leaflet_map;

        if (!window.userCircles) {{
            window.userCircles = [];
        }}

        if (!window.circleLayers) {{
            window.circleLayers = L.layerGroup().addTo(map);
        }}

        function updateCircles(e) {{
            let radii = {radii};  // List of radii in meters
            radii.forEach((radius, index) => {{
                if (window.userCircles[index]) {{
                    window.userCircles[index].setLatLng(e.latlng);
                }} else {{
                    let circle = L.circle(e.latlng, {{
                        radius: radius,
                        color: 'black',
                        fillColor: 'blue',
                        fillOpacity: 0.2
                    }});

                    circle.bindPopup("Radius: " + radius + " meters");
                    window.userCircles[index] = circle;
                    window.circleLayers.addLayer(circle);
                }}
            }});
        }}

        map.on("locationfound", updateCircles);

        // Add Layer Control
        var baseLayers = {{}};
        var overlays = {{}};
        
        let radii = {radii};
        radii.forEach((radius, index) => {{
            overlays["Circle " + radius + "m"] = window.userCircles[index];
        }});

        L.control.layers(baseLayers, overlays, {{ collapsed: false }}).addTo(map);
    }});
    </script>
    """.format(radii=radii)

    map_find_html = """
    <script>
    L.Map.addInitHook(function () {
        this.getContainer()._leaflet_map = this;
    });
    </script>
    """

    # Add the map_find_html to the map
    m.get_root().html.add_child(Element(map_find_html))
    # Add the JS script to the map
    m.get_root().html.add_child(Element(js))'''

def add_location_circles(m, radii):
    # JavaScript to update multiple circles dynamically with layer control
    js = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        var map = document.querySelector(".folium-map")._leaflet_map;

        if (!window.userCircles) {{
            window.userCircles = [];
        }}

        function updateCircles(e) {{
            let radii = {radii};  // List of radii in meters
            radii.forEach((radius, index) => {{
                if (window.userCircles[index]) {{
                    window.userCircles[index].setLatLng(e.latlng);
                }} else {{
                    let circle = L.circle(e.latlng, {{
                        radius: radius,
                        color: 'black',
                        fillColor: 'blue',
                        fillOpacity: 0.2
                    }}).bindPopup("Radius: " + radius + " meters");

                    window.userCircles[index] = circle;
                }}
            }});

            // Update layer group with userCircles
            if (window.circleLayerGroup) {{
                window.circleLayerGroup.clearLayers();
            }} else {{
                window.circleLayerGroup = L.layerGroup(window.userCircles).addTo(map);
            }}
            window.userCircles.forEach(circle => window.circleLayerGroup.addLayer(circle));
        }}

        map.on("locationfound", updateCircles);

        // Add Layer Control
        var baseLayers = {{}};
        var overlays = {{ "User Circles": window.circleLayerGroup }};
        L.control.layers(baseLayers, overlays, {{ collapsed: false }}).addTo(map);
    }});
    </script>
    """.format(radii=radii)

    map_find_html = """
    <script>
    L.Map.addInitHook(function () {
        this.getContainer()._leaflet_map = this;
    });
    </script>
    """

    # Add the map_find_html to the map
    m.get_root().html.add_child(Element(map_find_html))
    # Add the JS script to the map
    m.get_root().html.add_child(Element(js))

def add_location_circles2(m, radii, radii_text: list = None):
    # JavaScript to update multiple circles dynamically with layer control
    if radii_text is None:
        radii_text = ["Radius: " + str(radius) + " meters" for radius in radii]
    js = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        var map = document.querySelector(".folium-map")._leaflet_map;

        if (!window.userCircles) {{
            window.userCircles = [];
        }}

        if (!window.circleLayerGroup) {{
            window.circleLayerGroup = L.layerGroup().addTo(map);
            // Add custom attribute to the layer group
            window.circleLayerGroup.layer_name = "User Circles";
        }}

        function updateCircles(e) {{
            let radii = {radii};  // List of radii in meters
            let radii_text = {radii_text};  // List of radius text for popups
            radii.forEach((radius, index) => {{
                if (window.userCircles[index]) {{
                    window.userCircles[index].setLatLng(e.latlng);
                }} else {{
                    let circle = L.circle(e.latlng, {{
                        radius: radius,
                        color: 'black',
                        fillColor: 'blue',
                        fillOpacity: 0.2
                    }}).bindPopup(radii_text[index]);
                    // Add custom attribute to the circle
                    circle.circle_no = index;

                    window.userCircles[index] = circle;
                    window.circleLayerGroup.addLayer(circle);
                }}
            }});
        }}

        map.on("locationfound", updateCircles);

        // Add Layer Control
        //var baseLayers = {{}};
        //var overlays = {{ "User Circles": window.circleLayerGroup }};
        //L.control.layers(baseLayers, overlays, {{ collapsed: false }}).addTo(map);
    }});
    </script>
    """.format(radii=radii, radii_text=radii_text)

    map_find_html = """
    <script>
    L.Map.addInitHook(function () {
        this.getContainer()._leaflet_map = this;
    });
    </script>
    """

    # Add the map_find_html to the map
    m.get_root().html.add_child(Element(map_find_html))
    # Add the JS script to the map
    m.get_root().html.add_child(Element(js))


# TODO: Move add_location_circle2 into transit_map.py and move this file into folium_maps/
# TODO: This file is a mess lol

def add_location_circle2(m, radius, popup_str, circle_no: int = 1):
    # JavaScript to update the circle dynamically
    js = """
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        var map = document.querySelector(".folium-map")._leaflet_map;  

        function updateCircle(e) {{
            if (window.userCircle{circle_no}) {{
                window.userCircle{circle_no}.setLatLng(e.latlng);
            }} else {{
                window.userCircle{circle_no} = L.circle(e.latlng, {{
                    radius: {},  // 1 mile in meters
                    color: 'black',
                    fillColor: 'blue',
                    fillOpacity: 0.2
                }}).addTo(map);
                window.userCircle{circle_no}.bindPopup("{popup_str}");
            }}
        }}

        map.on("locationfound", updateCircle);
    }});
    </script>
    """.format(radius, circle_no=circle_no, popup_str=popup_str)

    map_find_html = """
    <script>
    L.Map.addInitHook(function () {
    // Store a reference of the Leaflet map object on the map container,
    // so that it could be retrieved from DOM selection.
    // https://leafletjs.com/reference-1.3.4.html#map-getcontainer
    this.getContainer()._leaflet_map = this;
    });
    </script>
    """

    # Add the map_find_html to the map
    m.get_root().html.add_child(Element(map_find_html))
    # Add the JS script to the map
    m.get_root().html.add_child(Element(js))

if __name__ == "__main__":
    import folium
    from folium.plugins import LocateControl

    # # # Create the folium map
    # # m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)  # Default to San Francisco

    # # # Add LocateControl
    # # LocateControl(auto_start=True).add_to(m)

    # # # JavaScript to update the circle dynamically
    # # js = """
    # # <script>
    # # function updateCircle(e) {
    # #     console.log("Update circle!");
    # #     if (window.userCircle) {
    # #         window.userCircle.setLatLng(e.latlng);
    # #     } else {
    # #         window.userCircle = L.circle(e.latlng, {
    # #             radius: 1609.34,  // 1 mile in meters
    # #             color: 'blue',
    # #             fillColor: 'blue',
    # #             fillOpacity: 0.2
    # #         }).addTo(this);
    # #     }
    # # }

    # # // Wait for the map to load
    # # document.addEventListener("DOMContentLoaded", function() {
    # #     var map = document.querySelector(".folium-map")._leaflet_map;
    # #     console.log(map);
    # #     map.on("locationfound", updateCircle);
    # # });
    # # </script>
    # # """

    # # # Add the JS script to the map
    # # m.get_root().html.add_child(folium.Element(js))

    # # Create the folium map
    # m = folium.Map(
    #     location=[37.7749, -122.4194], 
    #     zoom_start=13
    #     )  # Default to San Francisco

    # # Add LocateControl
    # LocateControl(auto_start=True).add_to(m)

    # # JavaScript to update the circle dynamically
    # js = """
    # <script>
    # document.addEventListener("DOMContentLoaded", function() {
    #     var map = document.querySelector(".folium-map")._leaflet_map;  

    #     function updateCircle(e) {
    #         if (window.userCircle) {
    #             window.userCircle.setLatLng(e.latlng);
    #         } else {
    #             window.userCircle = L.circle(e.latlng, {
    #                 radius: 1609.34,  // 1 mile in meters
    #                 color: 'blue',
    #                 fillColor: 'blue',
    #                 fillOpacity: 0.2
    #             }).addTo(map);
    #         }
    #     }

    #     map.on("locationfound", updateCircle);
    # });
    # </script>
    # """

    # map_find_html = """
    # <script>
    # L.Map.addInitHook(function () {
    # // Store a reference of the Leaflet map object on the map container,
    # // so that it could be retrieved from DOM selection.
    # // https://leafletjs.com/reference-1.3.4.html#map-getcontainer
    # this.getContainer()._leaflet_map = this;
    # });
    # </script>
    # """

    # # Add the map_find_html to the map
    # m.get_root().html.add_child(folium.Element(map_find_html))
    # # Add the JS script to the map
    # m.get_root().html.add_child(folium.Element(js))

    # # Display the map
    # m.save("location_test.html")
    import folium
    from folium.plugins import LocateControl
    from folium import Element

    def add_location_circle(m, radius):
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
                L.circle(e.latlng, {{
                    radius: {radius},  
                    color: 'blue',
                    fillColor: 'blue',
                    fillOpacity: 0.2
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

    # Create the map
    m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)

    # Add LocateControl
    LocateControl(auto_start=True).add_to(m)

    # Add the location circle (1 mile radius)
    location_layer = add_location_circle(m, radius=1609.34)

    # Add LayerControl to toggle the circle
    folium.LayerControl(collapsed=False).add_to(m)

    # Show the map
    m.save("location_test.html")

