
# This code is to test different ways of creating a coordinate class that has type hints in it.

from typing import NamedTuple
from pydantic import BaseModel, Field
from dataclasses import dataclass
import time
import random

# Define coordinate types
class CoordinateTuple(NamedTuple):
    lon: float
    lat: float

@dataclass
class CoordinateDataclass:
    lon: float
    lat: float

class CoordinatePydantic(BaseModel):
    lon: float = Field(..., ge=-180, le=180)
    lat: float = Field(..., ge=-90, le=90)

# Generate a million random points
NUM_POINTS = 1_000_000
data = [(random.uniform(-180, 180), random.uniform(-90, 90)) for _ in range(NUM_POINTS)]

# Benchmark raw tuples
start = time.time()
tuple_points = [(lon, lat) for lon, lat in data]
tuple_time = time.time() - start

# Benchmark NamedTuple
start = time.time()
namedtuple_points = [CoordinateTuple(lon, lat) for lon, lat in data]
namedtuple_time = time.time() - start

# Benchmark Dataclass
start = time.time()
dataclass_points = [CoordinateDataclass(lon, lat) for lon, lat in data]
dataclass_time = time.time() - start

# Benchmark Pydantic
start = time.time()
pydantic_points = [CoordinatePydantic(lon=lon, lat=lat) for lon, lat in data]
pydantic_time = time.time() - start

# Report results
print(f"Tuple: {tuple_time:.4f} sec")
print(f"NamedTuple: {namedtuple_time:.4f} sec")
print(f"Dataclass: {dataclass_time:.4f} sec")
print(f"Pydantic: {pydantic_time:.4f} sec")
