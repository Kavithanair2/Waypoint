"""Concrete trail types for the Waypoint domain engine."""

from waypoint_core.distance import Distance
from waypoint_core.mixins import PermitRequiredMixin, SeasonalAccessMixin
from waypoint_core.trail import Trail


class DayHike(Trail):
    """Represent a trail intended to be completed in one day."""

    def __init__(
            self,
            trail_id: int,
            name: str,
            distance: Distance,
            elevation_gain_m: float,
            difficulty: str,
    ) -> None:
        super().__init__(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
        )

    def estimated_time(self) -> float:
        """Estimate time using 4 km/h plus elevation adjustment."""
        distance_km = self.distance.convert("km").magnitude
        return distance_km / 4.0 + self.elevation_gain_m / 600.0

    def summary(self) -> str:
        """Return a readable day-hike summary."""
        return (
            f"Day hike: {self.name}, {self.distance}, "
            f"difficulty: {self.difficulty}"
        )


class BackpackingRoute(Trail):
    """Represent a multi-day backpacking route."""

    def __init__(
            self,
            trail_id: int,
            name: str,
            distance: Distance,
            elevation_gain_m: float,
            difficulty: str,
            days: int = 2,
    ) -> None:
        super().__init__(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
        )

        if isinstance(days, bool) or not isinstance(days, int):
            raise TypeError("Days must be an integer.")

        if days <= 0:
            raise ValueError("Days must be greater than zero.")

        self._days = days

    @property
    def days(self) -> int:
        """Return the planned number of days."""
        return self._days

    def estimated_time(self) -> float:
        """Estimate time using a slower pace and overnight adjustments."""
        distance_km = self.distance.convert("km").magnitude
        hiking_time = distance_km / 3.0
        elevation_time = self.elevation_gain_m / 500.0
        overnight_adjustment = max(self.days - 1, 0) * 0.5

        return hiking_time + elevation_time + overnight_adjustment

    def packing_list(self) -> list[str]:
        """Extend the common list with overnight equipment."""
        return super().packing_list() + [
            "tent",
            "sleeping bag",
            "camp stove",
        ]

    def summary(self) -> str:
        """Return a readable backpacking summary."""
        return (
            f"Backpacking route: {self.name}, {self.distance}, "
            f"{self.days} days, difficulty: {self.difficulty}"
        )


class TrailRun(Trail):
    """Represent a trail intended for running."""

    def __init__(
            self,
            trail_id: int,
            name: str,
            distance: Distance,
            elevation_gain_m: float,
            difficulty: str,
    ) -> None:
        super().__init__(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
        )

    def estimated_time(self) -> float:
        """Estimate time using 8 km/h plus elevation adjustment."""
        distance_km = self.distance.convert("km").magnitude
        return distance_km / 8.0 + self.elevation_gain_m / 800.0

    def summary(self) -> str:
        """Return a readable trail-run summary."""
        return (
            f"Trail run: {self.name}, {self.distance}, "
            f"difficulty: {self.difficulty}"
        )


class GuidedDayHike(DayHike):
    """Represent a day hike led by a named guide."""

    def __init__(
            self,
            trail_id: int,
            name: str,
            distance: Distance,
            elevation_gain_m: float,
            difficulty: str,
            guide_name: str,
    ) -> None:
        super().__init__(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
        )

        if not isinstance(guide_name, str):
            raise TypeError("Guide name must be a string.")

        normalized_guide_name = guide_name.strip()

        if not normalized_guide_name:
            raise ValueError("Guide name cannot be empty.")

        self._guide_name = normalized_guide_name

    @property
    def guide_name(self) -> str:
        """Return the guide's name."""
        return self._guide_name

    def summary(self) -> str:
        """Extend the day-hike summary with guide information."""
        return f"{super().summary()}, guide: {self.guide_name}"


class ManagedDayHike(SeasonalAccessMixin,PermitRequiredMixin,DayHike,):
    """Represent a managed hike with permit and seasonal restrictions."""

    pass