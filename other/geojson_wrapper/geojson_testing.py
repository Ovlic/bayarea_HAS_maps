from typing import Dict, Any, Optional, Type
from dataclasses import dataclass
from enum import Enum

# Assuming GeometryType is defined elsewhere, e.g., an Enum for geometry types
class GeometryType(Enum):
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"
    # Add other geometry types as needed

@dataclass
class Properties:
    """Base properties class that can be extended for specific feature types."""
    
    extra_fields: Dict[str, Any] = None

    def __post_init__(self):
        if self.extra_fields is None:
            self.extra_fields = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert the properties to a dictionary, including extra fields."""
        return {**self.__dict__, **self.extra_fields}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Properties":
        """Create a Properties object from a dictionary, handling extra fields."""
        extra_fields = {key: value for key, value in data.items() if key not in cls.__annotations__}
        properties = cls(**{key: value for key, value in data.items() if key in cls.__annotations__})
        properties.extra_fields = extra_fields
        return properties

class Feature:
    """Represents a single GeoJSON Feature."""

    def __init__(
        self, 
        geometry: GeometryType, 
        properties_obj: Optional[Properties] = None, 
        properties_dict: Optional[Dict[str, Any]] = None, 
        properties_cls: Type[Properties] = Properties
    ):
        """Initializes a GeoJSON Feature.

        Parameters
        ----------
        geometry : GeometryType
            The geometry type of the feature (Point, LineString, etc.), must be a valid `GeometryType` enum value.
        properties_obj : Optional[Properties]
            An instance of a user-defined properties class.
        properties_dict : Optional[Dict[str, Any]]
            A dictionary of properties to be dynamically converted to a properties object.
        properties_cls : Type[Properties]
            The class to use when instantiating properties from a dictionary. Defaults to `Properties`.
        """
        if not isinstance(geometry, GeometryType):
            raise ValueError(f"Invalid geometry type: {geometry}. Must be an instance of GeometryType.")

        self.geometry = geometry

        # Prevent both properties_obj and properties_dict from being used simultaneously
        if properties_obj and properties_dict:
            raise ValueError("Cannot provide both properties_obj and properties_dict. Choose one.")

        if properties_obj:
            self.properties = properties_obj
        elif properties_dict:
            self.properties = properties_cls.from_dict(properties_dict)  # Convert dictionary to class
        else:
            self.properties = properties_cls()  # Default empty properties

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Feature into a GeoJSON-compatible dictionary."""
        return {
            "type": "Feature",
            "geometry": self.geometry,  # Directly use the geometry string (enum value)
            "properties": self.properties.to_dict(),
        }

    def __repr__(self):
        """Returns a string representation of the Feature."""
        return f"Feature(geometry={self.geometry}, properties={self.properties})"


# Example data for properties
data = {
    "name": "Building A",
    "height": 100.0,
    "material": "Steel",
    "extra_attribute": "Value",  # This is an extra field
}

# Custom properties class
@dataclass
class BuildingProperties(Properties):
    name: str
    height: float
    material: str
    extra_fields: Dict[str, Any] = None  # Default for extra_fields

# Create a Feature with a dictionary of properties
feature = Feature(geometry=GeometryType.POINT, properties_cls=BuildingProperties, properties_dict=data)

# Print out the feature and its properties
print(feature)
print(feature.to_dict())

# Accessing extra fields
print(feature.properties.extra_fields)  # {'extra_attribute': 'Value'}
