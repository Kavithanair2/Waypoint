"""
Trail entity for the Week 7 Waypoint domain model.
"""

from collections.abc import Mapping
from typing import Any

from waypoint_core.distance import Distance


class Trail:
    """Represent a trail with validated identity and trail information."""

    ALLOWED_DIFFICULTIES = ("easy", "moderate", "hard", "expert")
    default_unit = "km"

    def __init__(
        self,
        trail_id: int,
        name: str,
        distance: Distance,
        elevation_gain_m: float,
        difficulty: str,
    ) -> None:
        self._trail_id = self.validate_trail_id(trail_id)
        self._name = self.validate_name(name)

        if not isinstance(distance, Distance):
            raise TypeError("distance must be a Distance object.")

        self._distance = distance
        self._elevation_gain_m = self.validate_elevation_gain(elevation_gain_m)
        self._difficulty = ""
        self.set_difficulty(difficulty)

    @property
    def trail_id(self) -> int:
        """Return the trail's unique identifier."""
        return self._trail_id

    @property
    def name(self) -> str:
        """Return the trail name."""
        return self._name


    @property
    def distance(self) -> Distance:
        """Return the trail distance."""
        return self._distance

    @property
    def elevation_gain_m(self) -> float:
        """Return the elevation gain in metres."""
        return self._elevation_gain_m

    @property
    def difficulty(self) -> str:
        """Return the validated difficulty."""
        return self._difficulty

    def set_difficulty(self, difficulty: str) -> None:
        """Change the difficulty only when the new value is valid."""
        self._difficulty = self.validate_difficulty(difficulty)

    @classmethod
    def set_default_unit(cls, unit: str) -> None:
        """Set the unit used by future dictionary-created trails."""
        cls.default_unit = Distance.validate_unit(unit)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Trail":
        """Create a Trail from an API-shaped dictionary."""
        if not isinstance(data, Mapping):
            raise TypeError("Trail data must be a mapping.")

        required_keys = {
            "id",
            "name",
            "distance",
            "elevation_gain_m",
            "difficulty",
        }

        missing_keys = required_keys.difference(data.keys())

        if missing_keys:
            missing_text = ", ".join(sorted(missing_keys))
            raise ValueError(f"Missing required trail data: {missing_text}.")

        unit = data.get("unit", cls.default_unit)


        return cls(
            trail_id=data["id"],
            name=data["name"],
            distance=Distance(data["distance"], unit),
            elevation_gain_m=data["elevation_gain_m"],
            difficulty=data["difficulty"],
        )

    @staticmethod
    def validate_trail_id(trail_id: int) -> int:
        """Validate a positive integer trail identifier."""
        if isinstance(trail_id, bool) or not isinstance(trail_id, int):
            raise TypeError("Trail id must be an integer.")

        if trail_id <= 0:
            raise ValueError("Trail id must be greater than zero.")

        return trail_id

    @staticmethod
    def validate_name(name: str) -> str:
        """Validate and normalize a trail name."""
        if not isinstance(name, str):
            raise TypeError("Trail name must be a string.")

        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Trail name cannot be empty.")

        return normalized_name

    @staticmethod
    def validate_elevation_gain(elevation_gain_m: float) -> float:
        """Validate a non-negative elevation gain."""
        if isinstance(elevation_gain_m, bool) or not isinstance(
            elevation_gain_m,
            (int, float),
        ):
            raise TypeError("Elevation gain must be a number.")

        if elevation_gain_m < 0:
            raise ValueError("Elevation gain cannot be negative.")

        return float(elevation_gain_m)


    @staticmethod
    def validate_difficulty(difficulty: str) -> str:
        """Validate and normalize a supported difficulty."""
        if not isinstance(difficulty, str):
            raise TypeError("Difficulty must be a string.")

        normalized_difficulty = difficulty.strip().lower()

        if normalized_difficulty not in Trail.ALLOWED_DIFFICULTIES:
            allowed = ", ".join(Trail.ALLOWED_DIFFICULTIES)
            raise ValueError(f"Difficulty must be one of: {allowed}.")

        return normalized_difficulty


    def __eq__(self, other: object) -> bool:
        """Compare trails using only their unique identifier."""
        if not isinstance(other, Trail):
            return NotImplemented

        return self.trail_id == other.trail_id
