"""Itinerary composition for the Waypoint domain model."""

from collections.abc import Iterable

from waypoint_core.distance import Distance
from waypoint_core.trail import Trail



class Itinerary:
    """Maintain an ordered and independent collection of trails."""

    def __init__(self, trails: Iterable[Trail] | None = None) -> None:
        self._trails: list[Trail] = []

        if trails is not None:
            for trail in trails:
                self.add_trail(trail)

    @property
    def trails(self) -> tuple[Trail, ...]:
        """Return an immutable view of the trails in their original order."""
        return tuple(self._trails)

    def add_trail(self, trail: Trail) -> None:
        """Add one valid Trail to the end of the itinerary."""
        if not isinstance(trail, Trail):
            raise TypeError("Only Trail objects can be added to an itinerary.")

        self._trails.append(trail)

    def total_distance(self, unit: str | None = None) -> Distance:
        """Calculate the combined trail distance in one selected unit."""
        if unit is None:
            if self._trails:
                target_unit = self._trails[0].distance.unit
            else:
                target_unit = "km"
        else:
            target_unit = Distance.validate_unit(unit)

        total_magnitude = 0.0

        for trail in self._trails:
            converted_distance = trail.distance.convert(target_unit)
            total_magnitude += converted_distance.magnitude

        return Distance(total_magnitude, target_unit)


    def __len__(self) -> int:
        """Return the number of trails in the itinerary."""
        return len(self._trails)