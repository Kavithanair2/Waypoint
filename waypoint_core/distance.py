"""
Distance value type for the Waypoint domain model.
"""

import math


class Distance:
    """Represent a non-negative distance measured in kilometres or miles."""

    VALID_UNITS = ("km", "mi")
    KM_PER_MILE = 1.609344

    def __init__(self, magnitude: float, unit: str) -> None:
        self._magnitude = self.validate_magnitude(magnitude)
        self._unit = self.validate_unit(unit)

    @property
    def magnitude(self) -> float:
        """Return the distance magnitude as a read-only value."""
        return self._magnitude

    @property
    def unit(self) -> str:
        """Return the distance unit as a read-only value."""
        return self._unit

    @staticmethod
    def validate_magnitude(magnitude: float) -> float:
        """Validate and return a non-negative numeric magnitude."""
        if isinstance(magnitude, bool) or not isinstance(magnitude, (int, float)):
            raise TypeError("Distance magnitude must be a number.")

        if magnitude < 0:
            raise ValueError("Distance magnitude cannot be negative.")

        return float(magnitude)

    @classmethod
    def validate_unit(cls, unit: str) -> str:
        """Validate and normalize a supported distance unit."""
        if not isinstance(unit, str):
            raise TypeError("Distance unit must be a string.")

        normalized_unit = unit.strip().lower()

        if normalized_unit not in cls.VALID_UNITS:
            raise ValueError("Distance unit must be 'km' or 'mi'.")

        return normalized_unit

    def convert(self, target_unit: str) -> "Distance":
        """Return a new Distance converted to the requested unit."""
        normalized_target = self.validate_unit(target_unit)

        if normalized_target == self.unit:
            return Distance(self.magnitude, self.unit)

        if self.unit == "km":
            converted_magnitude = self.magnitude / self.KM_PER_MILE
        else:
            converted_magnitude = self.magnitude * self.KM_PER_MILE

        return Distance(converted_magnitude, normalized_target)

    def _magnitude_in(self, unit: str) -> float:
        """Return this distance's magnitude expressed in the given unit."""
        return self.convert(unit).magnitude

    def __add__(self, other: object) -> "Distance":
        """Add distances and return the result in the left operand's unit."""
        if not isinstance(other, Distance):
            return NotImplemented

        other_magnitude = other._magnitude_in(self.unit)
        return Distance(self.magnitude + other_magnitude, self.unit)

    def __sub__(self, other: object) -> "Distance":
        """Subtract distances and return the result in the left operand's unit."""
        if not isinstance(other, Distance):
            return NotImplemented

        other_magnitude = other._magnitude_in(self.unit)
        result = self.magnitude - other_magnitude

        if result < 0:
            raise ValueError(
                "Distance subtraction cannot produce a negative value."
            )

        return Distance(result, self.unit)

    def __eq__(self, other: object) -> bool:
        """Compare distances after converting both values to kilometres."""
        if not isinstance(other, Distance):
            return NotImplemented

        return math.isclose(
            self._magnitude_in("km"),
            other._magnitude_in("km"),
            rel_tol=1e-9,
            abs_tol=1e-9,
        )

    def __lt__(self, other: object) -> bool:
        """Return whether this distance is shorter than another distance."""
        if not isinstance(other, Distance):
            return NotImplemented

        return self._magnitude_in("km") < other._magnitude_in("km")

    def __gt__(self, other: object) -> bool:
        """Return whether this distance is longer than another distance."""
        if not isinstance(other, Distance):
            return NotImplemented

        return self._magnitude_in("km") > other._magnitude_in("km")

    def __str__(self) -> str:
        """Return a readable distance for users."""
        return f"{self.magnitude:g} {self.unit}"

    def __repr__(self) -> str:
        """Return an unambiguous developer representation."""
        return (
            f"Distance(magnitude={self.magnitude!r}, "
            f"unit={self.unit!r})"
        )
