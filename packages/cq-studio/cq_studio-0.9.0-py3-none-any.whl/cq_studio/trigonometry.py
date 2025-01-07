__all__ = [
    "Coords",
    "angle_from_radius_and_chord_length",
    "chord_length_from_sagitta_and_radius",
    "radius_from_sagitta_and_chord_length",
    "sagitta",
    "sagitta_from_radius_and_arc_length",
    "vector",
]

import math


class Coords(list):
    """A fixed-size list for 2- or 3-dimensional Cartesian coordinates (x, y, z) with
    meaningful named attributes to access the individual values.
    """

    def __init__(self, x: float, y: float, z: float | None = None):
        super().__init__([x, y])
        if z is not None:
            self.append(z)

    @property
    def x(self) -> float:
        """Width."""
        return self[0]

    @property
    def y(self) -> float:
        """Depth."""
        return self[1]

    @property
    def z(self) -> float:
        """Height."""
        if len(self) < 3:
            raise ValueError(f"no z coordinate: {self}")
        return self[2]


def sagitta(radius: float, chord_length: float) -> float:
    """Calculate the height of an arc from its radius and chord half-length.

    Length is to the midpoint of the arc/chord, i.e. where its height is measured, not the
    length of the whole chord.
    """
    height = radius - math.sqrt((radius**2) - (chord_length**2))
    return height


def chord_length_from_sagitta_and_radius(sagitta: float, radius: float) -> float:
    """Calculate the half-length of a chord / width of an arc from its radius and height.

    Length is to the midpoint of the arc/chord, i.e. where its height is measured, not the
    length of the whole chord.
    """
    length = math.sqrt(2 * sagitta * radius - sagitta**2) / 2
    return length


def radius_from_sagitta_and_chord_length(sagitta: float, chord_length: float) -> float:
    """Calculate the radius of an arc from its chord half-length and sagitta.

    Length is to the midpoint of the arc/chord, i.e. where its height is measured, not the
    length of the whole chord.
    """
    radius = (sagitta**2 + chord_length**2) / (2 * sagitta)
    return radius


def sagitta_from_radius_and_arc_length(radius: float, arc_length: float) -> float:
    """Calculate the height of an arc from its radius and arc length.

    Arc length is measured like circumference, and with radius can be used to calculate the
    sagitta/arc height.
    """
    chord_length = radius * math.sin(arc_length / (2 * radius))
    return sagitta(radius, chord_length)


def angle_from_radius_and_chord_length(radius: float, chord_length: float) -> float:
    """Calculate the angle of a circle occupied by a chord of a given half-length.

    Length is to the midpoint of the arc/chord, i.e. where its height is measured, not the
    length of the whole chord.

    Return value is in degrees, not radians, as CadQuery uses degrees.
    """
    arc_height = sagitta(radius, chord_length)
    y = radius - arc_height
    x = chord_length
    angle = math.degrees(math.atan2(y, x))
    return 2 * angle


def vector(angle: float, magnitude: float, start: Coords = Coords(0, 0)) -> Coords:
    """From a vector (or polar coordinate), calculate the equivalent Cartesian coordinates,
    optionally starting from a point other than the origin.
    """
    assert -360 < angle < 360
    a = math.radians(angle)
    x = magnitude * math.cos(a)
    y = magnitude * math.sin(a)
    return Coords(start.x + x, start.y + y)
