
from enum import Enum

class TestEnum(Enum):
    A = 1
    B = 2
    C = 3

def test_func(enum: TestEnum):
    if not isinstance(enum, TestEnum):
        raise ValueError("Invalid enum value")
    print(enum)


test_func(TestEnum.A)
test_func(TestEnum.B)
test_func(TestEnum.C)
test_func(4) 