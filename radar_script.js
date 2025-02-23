
document.addEventListener("DOMContentLoaded", function() {
    var map = document.querySelector(".folium-map")._leaflet_map;

    // Loop through layers and add to the appropriate object
    
    var bart_lines = {};
    var muni_lines = {};
    var commuter_lines = {};
    var other_layers = [];
    var station_markers_temp = {};

    var borders = [];
    var base_layers = [];

    var overlay_layers_temp = {};

    var muni_names = ["MUNI 038R", "MUNI F", "MUNI J", "MUNI K", "MUNI L", "MUNI M", "MUNI N", "MUNI T", "MUNI Powell-Hyde Cable Car", "MUNI Powell-Mason Cable Car", "MUNI California Cable Car"];
    var commuter_names = ["Caltrain", "ACE"];
    var border_names = ["San Francisco County Boundary"];


    // Instead of looping through map._layers, we can use map.eachLayer

    map.eachLayer(function(layer) {
        if (layer instanceof L.Marker){
            // It's probably a station marker
            // if (Object.hasOwn(layer, "name")){
            //     console.log("Marker: "+layer.name);
            // }
            // add to the station_markers_temp object
            // Check if the line is in the station_markers_temp object
            // If it is, append the station to the list
            // If it isn't, create a new list with the station
            if (station_markers_temp.hasOwnProperty(layer.line)) {
                console.log("Layer line: "+layer.line + "; Layer operator: "+layer.operator);
                station_markers_temp[layer.line].push(layer);
            } else {
                station_markers_temp[layer.line] = [layer];
            }
            // Add to overlay_layers_temp
            if (overlay_layers_temp.hasOwnProperty(layer.operator)) {
                if (overlay_layers_temp[layer.operator].lines.hasOwnProperty(layer.line)) {
                    overlay_layers_temp[layer.operator].lines[layer.line].stations.push(layer);
                }
                else {
                    overlay_layers_temp[layer.operator].lines[layer.line] = {layers: [], stations: [layer]};
                }
            } else {
                overlay_layers_temp[layer.operator] = {lines: {}};
                overlay_layers_temp[layer.operator].lines[layer.line] = {layers: [], stations: [layer]};
            }

        } else if (layer instanceof L.Polyline){
            // It's probably a transit line
            // Check the tooltip (after removing all the spaces, <div>, </div>, and \n) and see if it's in the list of names: "MUNI 038R", "MUNI F", "MUNI J", "MUNI K", "MUNI L", "MUNI M", "MUNI N", "MUNI T", "MUNI Powell-Hyde Cable Car", "MUNI Powell-Mason Cable Car", "MUNI California Cable Car", "BART Blue-N", "BART Blue-S", "BART Green-N", "BART Green-S", "BART Orange-N", "BART Orange-S", "BART Red-N", "BART Red-S", "BART Yellow-N", "BART Yellow-S", "BART Beige-N", "BART Beige-S", "Caltrain", "Caltrain South County", "VTA Blue Line", "VTA Green Line", "VTA Orange Line", "ACE"
            // If it is, append it to the appropriate list
            // If it isn't, append it to the other_layers list
            var route_names = ["MUNI 038R", "MUNI F", "MUNI J", "MUNI K", "MUNI L", "MUNI M", "MUNI N", "MUNI T", "MUNI Powell-Hyde Cable Car", "MUNI Powell-Mason Cable Car", "MUNI California Cable Car", "BART Blue-N", "BART Blue-S", "BART Green-N", "BART Green-S", "BART Orange-N", "BART Orange-S", "BART Red-N", "BART Red-S", "BART Yellow-N", "BART Yellow-S", "BART Beige-N", "BART Beige-S", "Caltrain", "Caltrain South County", "VTA Blue Line", "VTA Green Line", "VTA Orange Line", "ACE"];
            // Check the tooltip of the layer
            if (layer.getTooltip() == null) {
                // Add to the other_layers list
                console.log("Layer has no tooltip");
                //console.log(layer);
                other_layers.push(layer);
                return;
            }
            var route_name = layer.getTooltip().getContent().replace(/<div>|<\/div>|\n/g, "");
            if (route_names.includes(route_name)) {
                if (route_name.includes("MUNI")) {
                    if (muni_lines.hasOwnProperty(route_name)) {
                        muni_lines[route_name].push(layer);
                    } else {
                        muni_lines[route_name] = [layer];
                    }
                    // Add to overlay_layers_temp
                    if (overlay_layers_temp.hasOwnProperty(layer.operator)) {
                        if (overlay_layers_temp[layer.operator].lines.hasOwnProperty(route_name)) {
                            overlay_layers_temp[layer.operator].lines[route_name].layers.push(layer);
                        }
                        else {
                            overlay_layers_temp[layer.operator].lines[route_name] = {layers: [layer], stations: []};
                        }
                    } else {
                        overlay_layers_temp[layer.operator] = {lines: {}};
                        overlay_layers_temp[layer.operator].lines[route_name] = {layers: [layer], stations: []};
                    }

                    // muni_lines.push(layer);
                } else if (route_name.includes("BART")) {
                    if (bart_lines.hasOwnProperty(route_name)) {
                        bart_lines[route_name].push(layer);
                    } else {
                        bart_lines[route_name] = [layer];
                    }
                    // Add to overlay_layers_temp
                    if (overlay_layers_temp.hasOwnProperty(layer.operator)) {
                        if (overlay_layers_temp[layer.operator].lines.hasOwnProperty(route_name)) {
                            overlay_layers_temp[layer.operator].lines[route_name].layers.push(layer);
                        }
                        else {
                            overlay_layers_temp[layer.operator].lines[route_name] = {layers: [layer], stations: []};
                        }
                    } else {
                        overlay_layers_temp[layer.operator] = {lines: {}};
                        overlay_layers_temp[layer.operator].lines[route_name] = {layers: [layer], stations: []};
                    }
                    //bart_lines.push(layer);
                } else if (route_name.includes("Caltrain") || route_name.includes("ACE")) {
                    if (commuter_lines.hasOwnProperty(route_name)) {
                        console.log("Commuter line exists: "+route_name);
                        commuter_lines[route_name].push(layer);
                    } else {
                        commuter_lines[route_name] = [layer];
                    }
                    // Add to overlay_layers_temp
                    if (overlay_layers_temp.hasOwnProperty(layer.operator)) {
                        if (overlay_layers_temp[layer.operator].lines.hasOwnProperty(route_name)) {
                            overlay_layers_temp[layer.operator].lines[route_name].layers.push(layer);
                        }
                        else {
                            overlay_layers_temp[layer.operator].lines[route_name] = {layers: [layer], stations: []};
                        }
                    } else {
                        overlay_layers_temp[layer.operator] = {lines: {}};
                        overlay_layers_temp[layer.operator].lines[route_name] = {layers: [layer], stations: []};
                    }
                    //commuter_lines.push(layer);
                }
            } else {
                other_layers.push({label: route_name, layer: layer});
            }
        } else if (layer instanceof L.TileLayer){
            // Add to the base_layers list
            base_layers.push({label: layer.tile_name, layer: layer});
            // console.log("TileLayer: "+layer.url);    
        } else if (layer instanceof L.GeoJSON){
            console.log("GeoJSON!");
            //console.log(layer);
            // To get the info that we need, we need to access the layer's sublayers' properties
            // We can loop through the layer's _layers attribute

            function add_to_list(name, layer){
                var muni_line_names = ["38R", "F", "J", "K", "L", "M", "N", "T", "Powell-Hyde Cable Car", "Powell-Mason Cable Car", "California Cable Car"];
                var bart_line_names = ["Blue-N", "Blue-S", "Green-N", "Green-S", "Orange-N", "Orange-S", "Red-N", "Red-S", "Yellow-N", "Yellow-S", "Beige-N", "Beige-S"];
                var commuter_line_names = ["Caltrain", "Caltrain South County", "VTA Blue Line", "VTA Green Line", "VTA Orange Line", "ACE"];
                if (muni_line_names.includes(name)) {
                    if (muni_lines.hasOwnProperty(name)) {
                        muni_lines[name].push(layer);
                    } else {
                        muni_lines[name] = [layer];
                    }
                } else if (bart_line_names.includes(name)) {
                    if (bart_lines.hasOwnProperty(name)) {
                        bart_lines[name].push(layer);
                    } else {
                        bart_lines[name] = [layer];
                    }
                } else if (commuter_line_names.includes(name)) {
                    if (commuter_lines.hasOwnProperty(name)) {
                        commuter_lines[name].push(layer);
                    } else {
                        commuter_lines[name] = [layer];
                    }
                }
                // Add to overlay_layers_temp
                var operator;
                if (name == "Caltrain Peninsula Subdivision") {
                    operator = "Caltrain";
                }
                if (overlay_layers_temp.hasOwnProperty(layer.operator)) {
                    if (overlay_layers_temp[layer.operator].lines.hasOwnProperty(name)) {
                        overlay_layers_temp[layer.operator].lines[name].layers.push(layer);
                    }
                    else {
                        overlay_layers_temp[layer.operator].lines[name] = {layers: [layer], stations: []};
                    }
                } else {
                    overlay_layers_temp[layer.operator] = {lines: {}};
                    overlay_layers_temp[layer.operator].lines[name] = {layers: [layer], stations: []};
                }
            }



            for (var key in layer._layers) {
                let sublayer = layer._layers[key];
                console.log(sublayer);
                // Properties
                // Check if the sublayer.feature.properties.route_name attribute exists
                // If it does, check if it's in the list of route names
                if (sublayer.feature.properties.route_name) {
                    console.log("Route: "+sublayer.feature.properties.route_name);
                    // Call the add_to_list function
                    add_to_list(sublayer.feature.properties.route_name, sublayer);
                } else if (sublayer.feature.properties.name) {
                    console.log("Route: "+sublayer.feature.properties.name);
                    if (sublayer.feature.properties.name == "Caltrain Peninsula Subdivision") {
                        sublayer.feature.properties.route_name = "Caltrain";
                    }
                    add_to_list(sublayer.feature.properties.name, sublayer);
                } else {
                    console.log("No route name was found, printing properties");
                    console.log(sublayer.feature.properties);
                    // Add to the other_layers list
                    other_layers.push(sublayer);
                }
            }
                
        } else {
            // Add to the other_layers list
            other_layers.push(layer);

            // if (Object.hasOwn(layer, "name")){
            //     console.log(type(layer) + ": "+layer.name);
            // } else {
            //     console.log(type(layer) + ": undefined")
            // }
        }
    });

    var station_markers = [];
    // Loop through the station_markers_temp object for each key make all it's values into a layergroup and add it to the list
    console.log("Length: "+Object.keys(station_markers_temp).length);
    console.log(station_markers_temp);
    for (var key in station_markers_temp) {
        // use the layer's "layer" attribute to create a layergroup
        var layer_group = L.layerGroup(station_markers_temp[key]);
        console.log("Station Key: "+key);
        station_markers.push({label: key, layer: layer_group});
    }

    // Now do the same for bart_lines, muni_lines, and commuter_lines
    var bart_lines_list = [];
    for (var key in bart_lines) {
        var layer_group = L.layerGroup(bart_lines[key]);
        bart_lines_list.push({label: key, layer: layer_group});
    }

    var muni_lines_list = [];
    for (var key in muni_lines) {
        var layer_group = L.layerGroup(muni_lines[key]);
        muni_lines_list.push({label: key, layer: layer_group});
    }

    var commuter_lines_list = [];
    for (var key in commuter_lines) {
        var layer_group = L.layerGroup(commuter_lines[key]);
        commuter_lines_list.push({label: key, layer: layer_group});
    }

    /*
    for (var key in map._layers) {
        let layer = map._layers[key];
        // There is an attribute called name and we can check whether its in a list of names
        // First check whether the _tiles attribute exists
        // Then append it to the appropriate list in this format:
        // {label: 'Layer Name', layer: layer}

        // If the layer is a tile layer
        if (layer._tiles) {
            base_layers.push({label: layer.tile_name, layer: layer});
        
        
        } else if (layer.name && muni_names.includes(layer.name)) {
            muni_lines.push({label: layer.name, layer: layer});
        } else if (layer.name && commuter_names.includes(layer.name)) {
            commuter_lines.push({label: layer.name, layer: layer});
        } else if (layer.name && border_names.includes(layer.name)) {
            borders.push({label: layer.name, layer: layer});
        } else {
            // Now we check for stations
            // Check the "_layers" attribute of the layer, and 
            
            other_layers.push({label: layer.name, layer: layer});
        }
    }

    // Now we have all the layers in their respective objects
    // Now we can add them to the LayerControl

    var overlay_layers = {
        label: 'Overlay Layers',
        children: [
            {
                label: 'Transit Lines',
                children: [
                    {
                        label: 'MUNI',
                        children: muni_lines
                    },
                    {
                        label: 'Commuter',
                        children: commuter_lines
                    }
                ]
            },
            {
                label: 'Borders',
                children: borders
            },
            {
                label: 'Other',
                children: other_layers
            }
        ]
    };*/

    var base_layers = {
        label: 'Base Layers',
        children: base_layers
    };

    var overlay_layers = {
        label: 'Overlay Layers',
        selectAllCheckbox: 'Un/select all',
        children: [
            {
                label: 'Transit Lines',
                selectAllCheckbox: true,
                children: [
                    {
                        label: 'BART',
                        selectAllCheckbox: true,
                        children: bart_lines_list
                    },
                    {
                        label: 'MUNI',
                        selectAllCheckbox: true,
                        children: muni_lines_list
                    },
                    {
                        label: 'Commuter',
                        selectAllCheckbox: true,
                        children: commuter_lines_list
                    }
                ]
            },
            {
                label: 'Stations',
                selectAllCheckbox: true,
                children: station_markers
            },
            {
                label: 'Other',
                selectAllCheckbox: true,
                children: other_layers
            }
        ]
    };

    var treeControl = L.control.layers.tree(base_layers, overlay_layers, {
        namedToggle: true,
        selectorBack: false,
        collapsed: false
    })
    treeControl.addTo(map).collapseTree().expandSelected();
    console.log(muni_lines);
    console.log(bart_lines);
    console.log(commuter_lines);

    // Convert overlay_layers_temp to an object that can be used by the LayerControl
    // Format: Operator name -> Line name -> lines, stations
    // console.log("Overlay Layers Temp");
    // console.log(overlay_layers_temp);

    // var overlay_layers = {
    //     label: 'Overlay Layers',
    //     selectAllCheckbox: 'Un/select all',
    //     children: []
    // };
    // // Combine all stations into a layer group and all line layers into another layer group
    // for (var key in overlay_layers_temp) {
    //     var operator = overlay_layers_temp[key];
    //     var operator_lines = [];
    //     for (var line in operator.lines) {
    //         var line_obj = operator.lines[line];
    //         var line_layers = line_obj.layers;
    //         var line_stations = line_obj.stations;
    //         var new_line_layers = L.layerGroup(line_layers);
    //         var new_line_stations = L.layerGroup(line_stations);

    //         operator_lines.push({
    //             label: line,
    //             selectAllCheckbox: true,
    //             collapsed: true,
    //             children: [
    //                 {
    //                     label: 'Lines',
    //                     selectAllCheckbox: true,
    //                     collapsed: true,
    //                     layer: new_line_layers
    //                 },
    //                 {
    //                     label: 'Stations',
    //                     selectAllCheckbox: true,
    //                     collapsed: true,
    //                     layer: new_line_stations
    //                 }
    //             ]
    //         });
    //     }
    //     overlay_layers.children.push({label: key, children: operator_lines});
    // }
    // // Add other_layers
    // overlay_layers.children.push({label: 'Other', children: other_layers});

    // var treeControl = L.control.layers.tree(base_layers, overlay_layers, {
    //     namedToggle: true,
    //     selectorBack: false,
    //     collapsed: false
    // })
    // treeControl.addTo(map).collapseTree().expandSelected();


});