
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Union
# Feature types

class BaseEnum(Enum):
    def __str__(self):
        return self.name


class GeometryType(BaseEnum):
    point = "Point"
    linestring = "LineString"
    polygon = "Polygon"
    multipoint = "MultiPoint"
    multilinestring = "MultiLineString"
    multipolygon = "MultiPolygon"
    geometrycollection = "GeometryCollection"


@dataclass
class Coordinates:
    """Represents geographical coordinates with latitude and longitude.

    Attributes
    ----------
    lon : float
        Longitude, ranging from -180 to 180 degrees.
    lat : float
        Latitude, ranging from -90 to 90 degrees.
    """

    lon: float = field(metadata={"doc": "Longitude, ranging from -180 to 180 degrees."})
    lat: float = field(metadata={"doc": "Latitude, ranging from -90 to 90 degrees."})

    def __str__(self) -> str:
        """Returns a string representation of the coordinates in the format (latitude, longitude)."""
        return f"({self.lat}, {self.lon})"

    def as_dict(self) -> dict:
        """Returns coordinates as a dictionary.

        Returns
        -------
        dict
            A dictionary with 'lat' and 'lon' as keys, representing latitude and longitude, respectively.
        """
        return {"lat": self.lat, "lon": self.lon}
    
    def to_json(self) -> List[float, float]:
        """Returns coordinates as a list.

        Returns
        -------
        List[float, float]
            A list containing latitude and longitude as its elements.
        """
        return [self.lat, self.lon]
    







# Use 
if __name__ == '__main__':
    from discord import enums
    pass