
import folium, json
from transit_map import op_to_name
from utils import makeBeautifyIcon

class Station:
    def __init__(self, stop, line_id, op):
        """stop should be from stations[op][line_id]["Contents"]["dataObjects"]["ScheduledStopPoint"]"""
        self.stop = stop
        self.line_id = line_id
        self.op = op

        # Load colors
        with open('data/colors.json', 'r') as f:
            self.colors = json.loads(f.read())

        # Get station properties
        self.lat = float(self.stop["Location"]["Latitude"])
        self.lon = float(self.stop["Location"]["Longitude"])
        self.id = self.stop["id"]
        self.name = self.stop["Name"]

        # Get connections if it exists
        self.connections = self.stop.get("connections", None)

    @classmethod
    def from_feature(cls, feature, line_id, op):
        # stop['id'], stop['Name'], stop['Location']['Latitude'], stop['Location']['Longitude']
        stop = {}
        stop['Name'] = feature["properties"]["name"]
        stop['id'] = feature["properties"].get('id', None) # Not always present
        the_op = feature["properties"].get('operator', op)
        stop['Location'] = {
            "Latitude": feature["geometry"]["coordinates"][1],
            "Longitude": feature["geometry"]["coordinates"][0]
        }
        if "connections" in feature["properties"]:
            stop["connections"] = feature["properties"]["connections"]

        return cls(stop, line_id, the_op)



    def to_marker(self):
        if self.connections:
            # print(self.connections)
            html = ""
            white_lines = ["L", "M", "N", "38R", "T", "Red", "Express", "CC", "ACETrain", "SMART", "Red Line AirTrain"]
            for op, connections in self.connections.items():
                for connection in connections:
                    if op == "BA":
                        color_fix = "-N"
                    else:
                        color_fix = ""

                    if connection in white_lines:
                        text_color = "white"
                    else:
                        text_color = "black"
                    # if connection in ["J", "K", "L", "M", "N"]: # MUNI
                    #     html += f"""<span style="background-color: {self.colors["SF"][connection]}; color: {"white" if connection in ["L", "M", "N", "38R", "T"] else "black"}";>{connection} {"Bus" if connection == "38R" else "Line"}</span>, """
                    # else:
                    if op == "SI":
                        color_str = (f'{connection}{color_fix}')[:-9]
                    else:
                        color_str = f'{connection}{color_fix}'

                    #print(f"op: {op}, connection: {connection}")
                    html += f"""<span style="background-color: {self.colors[op][color_str]}; color: {text_color}";>{connection}</span>, """
        
        else:
            html = f"""<span style="background-color: {self.colors[self.op][self.line_id]}; color: {"white" if self.line_id in ["CC", "ACETrain", "SMART"] else "black"}";>{self.line_id}</span>, """
        html = html[:-2]
        html += "</p>"

        p = folium.Popup(
            f"<p><b>Station</b>: {self.name}</p><br style='content: \" \";'><p><b>Line</b>: {html}</p><br style='content: \" \";'><p><b>Operator</b>: {op_to_name(self.op)}</p><a target=\"_blank\" href='https://ovlic.com/bayarea_HAS_maps/maps/point_25_mile/{self.op}/{self.line_id}/{self.id.replace(' ', '_')}.html'><b>View Station Map</b></a>",
            max_width=265
        )
        return folium.Marker(
            location=[self.lat, self.lon],
            popup=p,#stop['Name'],
            icon=makeBeautifyIcon(
                icon=None,
                border_color="#000000",
                border_width=3,
                text_color="#b3334f",
                icon_shape="circle",
                inner_icon_style="opacity: 0;",
                icon_size=[13, 13],
            ),
            # TESTING (edited folium Maker class)
            name=f"{op_to_name(self.op)} {self.line_id}",
            operator=self.op,
            line=self.line_id
            # line=f"{line_id}"
        )
    
    def to_json(self):
        return {
            "type": "Feature",
            "properties": {
                "name": self.name,
                "id": self.id,
                "line_id": self.line_id,
                "operator": self.op,
                "connections": self.connections
            },
            "geometry": {
                "type": "Point",
                "coordinates": [self.lon, self.lat]
            }
        }


class Line:
    def __init__(self, coords, operator, line_id, properties=None):
        self.coords = coords
        self.operator = operator
        self.line_id = line_id
        self.properties = properties

        # Load colors
        with open('data/colors.json', 'r') as f:
            self.colors = json.loads(f.read())

        # print(self.operator, self.line_id)
        
        # self.color = getattr(self.colors[self.operator], self.line_id, "#000000")
        if self.operator not in self.colors:
            print(f"Operator {self.operator} not found in colors.json")
            self.color = "#000000"
        elif self.line_id not in self.colors[self.operator]:
            print(f"Line {self.line_id} not found in {self.operator}")
            self.color = "#000000"
        else:
            self.color = self.colors[self.operator][self.line_id]
        # self.colors[self.operator][self.line_id]
        
        # if hasattr(self.colors[self.operator], self.line_id):
            # self.color = self.colors[self.operator][self.line_id]
        # else:
            # self.color = "#000000"
        

        # self.color = self.colors[self.operator][self.line_id]
        self.tooltip = f"{op_to_name(self.operator)} {self.line_id}"
        self.name = f"{op_to_name(self.operator)} {self.line_id}"

    @classmethod
    def from_feature(cls, feature, operator, line_id):
        # Get line properties
        coords = []
        for pos in feature["geometry"]["coordinates"]:
            try:
                # coords.append([pos[1], pos[0]])
                coords.append([pos[0], pos[1]])
            except Exception as e:
                print("Error in Line.from_feature")
                print(operator)
                print(line_id)
                print(pos)
                print(feature["geometry"]["coordinates"])
                raise e
        
        return cls(coords, operator, line_id, feature["properties"])

    def to_polyline(self):
        # print(self.colors[self.operator])
        # # Check if line_id is in colors[operator]
        # if self.line_id not in self.colors[self.operator]:
        #     print(f"Line {self.line_id} not found in {self.operator}")
        # else:
        #     print(f"Line {self.line_id} found in {self.operator}")
        # print(f"'{self.operator}'")
        # print(f"'{self.line_id}'")
        # print(f"'{self.color}'")
        # print(self.colors[self.operator][self.line_id])
        return folium.PolyLine(
            self.coords, 
            color=self.color, 
            tooltip=self.tooltip,
            name=self.name,
            weight=4,
            operator=self.operator,
            line=self.line_id
        )
    
    def to_json(self):
        # Fix stupid coordinate problems by checking whether the coordinates are in the right order (bigger number, negative number)
        coords = []
        for coord in self.coords:
            if coord[0] > coord[1]:
                coords.append([coord[0], coord[1]])
            else:
                coords.append([coord[1], coord[0]])
        self.coords = coords
        return {
            "type": "Feature",
            "properties": self.properties,
            "geometry": {
                "type": "LineString",
                "coordinates": self.coords
            }
        }
    

