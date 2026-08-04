"""
Distance value type for the Waypoint domain model.
"""


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