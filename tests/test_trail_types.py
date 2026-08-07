"""Unit tests for concrete Waypoint trail types."""

import unittest

from waypoint_core.distance import Distance
from waypoint_core.trail import Trail
from waypoint_core.trail_types import (
    BackpackingRoute,
    DayHike,
    GuidedDayHike,
    TrailRun,
)


class TrailTypeTests(unittest.TestCase):
    """Test concrete trail calculations, summaries, and inheritance."""

    def test_day_hike_estimated_time(self) -> None:
        trail = DayHike(
            trail_id=301,
            name="Forest View",
            distance=Distance(8, "km"),
            elevation_gain_m=600,
            difficulty="moderate",
        )

        self.assertAlmostEqual(trail.estimated_time(), 3.0)

    def test_backpacking_route_estimated_time(self) -> None:
        trail = BackpackingRoute(
            trail_id=302,
            name="Mountain Circuit",
            distance=Distance(12, "km"),
            elevation_gain_m=500,
            difficulty="hard",
            days=3,
        )

        self.assertAlmostEqual(trail.estimated_time(), 6.0)

    def test_trail_run_estimated_time(self) -> None:
        trail = TrailRun(
            trail_id=303,
            name="River Sprint",
            distance=Distance(8, "km"),
            elevation_gain_m=800,
            difficulty="moderate",
        )

        self.assertAlmostEqual(trail.estimated_time(), 2.0)

    def test_summaries_identify_each_concrete_type(self) -> None:
        day_hike = DayHike(
            trail_id=304,
            name="Pine Walk",
            distance=Distance(5, "km"),
            elevation_gain_m=100,
            difficulty="easy",
        )
        backpacking_route = BackpackingRoute(
            trail_id=305,
            name="Highland Route",
            distance=Distance(20, "km"),
            elevation_gain_m=900,
            difficulty="hard",
            days=2,
        )
        trail_run = TrailRun(
            trail_id=306,
            name="Creek Run",
            distance=Distance(6, "km"),
            elevation_gain_m=150,
            difficulty="moderate",
        )

        self.assertIn("Day hike:", day_hike.summary())
        self.assertIn("Backpacking route:", backpacking_route.summary())
        self.assertIn("Trail run:", trail_run.summary())

    def test_backpacking_packing_list_extends_base_list(self) -> None:
        trail = BackpackingRoute(
            trail_id=307,
            name="Overnight Ridge",
            distance=Distance(18, "km"),
            elevation_gain_m=700,
            difficulty="hard",
            days=2,
        )

        equipment = trail.packing_list()

        self.assertIn("water", equipment)
        self.assertIn("map", equipment)
        self.assertIn("first-aid kit", equipment)
        self.assertIn("tent", equipment)
        self.assertIn("sleeping bag", equipment)
        self.assertIn("camp stove", equipment)

    def test_guided_day_hike_extends_parent_summary(self) -> None:
        trail = GuidedDayHike(
            trail_id=308,
            name="Guided Lookout",
            distance=Distance(7, "km"),
            elevation_gain_m=250,
            difficulty="moderate",
            guide_name="Maya Singh",
        )

        summary = trail.summary()

        self.assertIn("Day hike:", summary)
        self.assertIn("Guided Lookout", summary)
        self.assertIn("guide: Maya Singh", summary)

    def test_guided_day_hike_has_two_inheritance_levels(self) -> None:
        trail = GuidedDayHike(
            trail_id=309,
            name="Valley Tour",
            distance=Distance(4, "km"),
            elevation_gain_m=80,
            difficulty="easy",
            guide_name="Alex Chen",
        )

        self.assertIsInstance(trail, GuidedDayHike)
        self.assertIsInstance(trail, DayHike)
        self.assertIsInstance(trail, Trail)

    def test_backpacking_days_are_validated(self) -> None:
        with self.assertRaises(TypeError):
            BackpackingRoute(
                trail_id=310,
                name="Invalid Route",
                distance=Distance(10, "km"),
                elevation_gain_m=300,
                difficulty="moderate",
                days=True,
            )

        with self.assertRaises(ValueError):
            BackpackingRoute(
                trail_id=311,
                name="Zero-Day Route",
                distance=Distance(10, "km"),
                elevation_gain_m=300,
                difficulty="moderate",
                days=0,
            )

    def test_guided_day_hike_rejects_empty_guide_name(self) -> None:
        with self.assertRaises(ValueError):
            GuidedDayHike(
                trail_id=312,
                name="Unnamed Guide Hike",
                distance=Distance(5, "km"),
                elevation_gain_m=120,
                difficulty="easy",
                guide_name="   ",
            )


if __name__ == "__main__":
    unittest.main()