from dataclasses import dataclass


@dataclass
class Vector:
    x: int
    y: int

    # v is of type Vector
    def __mul__(self, v: "Vector"):
        return Vector(self.x * v.x, self.y * v.x)

    def __add__(self, v: "Vector"):
        return Vector(self.x + v.x, self.y + v.y)

    def __sub__(self, v: "Vector"):
        return Vector(self.x - v.x, self.y - v.y)

    def __hash__(self):
        return id(self)

    # misc vector methods
    def scale(self, s: int):
        return Vector(self.x * s, self.y * s)
