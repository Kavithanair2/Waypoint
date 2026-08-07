"""Unit tests for polymorphic and duck-typed trail reporting."""

import unittest

from waypoint_core.distance import Distance
from waypoint_core.reporting import build_trail_report
from waypoint_core.trail import Trail
from waypoint_core.trail_types import (
    BackpackingRoute,
    DayHike,
    TrailRun,
)


class FakeTrail:
    """Provide trail-like behaviour without inheriting from Trail."""

    def __init__(self, name: str, hours: float) -> None:
        self.name = name
        self.hours = hours

    def summary(self) -> str:
        """Return a simple fake-trail summary."""
        return f"Fake trail: {self.name}"

    def estimated_time(self) -> float:
        """Return the configured test duration."""
        return self.hours


class ReportingTests(unittest.TestCase):
    """Test polymorphism and duck typing in trail reports."""

    def test_polymorphic_loop_handles_real_trail_types(self) -> None:
        trails = [
            DayHike(
                trail_id=501,
                name="Forest Walk",
                distance=Distance(8, "km"),
                elevation_gain_m=600,
                difficulty="moderate",
            ),
            BackpackingRoute(
                trail_id=502,
                name="Mountain Route",
                distance=Distance(12, "km"),
                elevation_gain_m=500,
                difficulty="hard",
                days=3,
            ),
            TrailRun(
                trail_id=503,
                name="River Run",
                distance=Distance(8, "km"),
                elevation_gain_m=800,
                difficulty="moderate",
            ),
        ]

        report = build_trail_report(trails)

        self.assertEqual(len(report), 3)
        self.assertIn("Day hike: Forest Walk", report[0])
        self.assertIn("Backpacking route: Mountain Route", report[1])
        self.assertIn("Trail run: River Run", report[2])

    def test_fake_trail_works_without_inheriting_from_trail(self) -> None:
        fake_trail = FakeTrail("Practice Route", 1.25)

        report = build_trail_report([fake_trail])

        self.assertNotIsInstance(fake_trail, Trail)
        self.assertEqual(
            report,
            [
                "Fake trail: Practice Route | "
                "estimated time: 1.25 hours"
            ],
        )

    def test_real_and_fake_trails_work_in_the_same_loop(self) -> None:
        real_trail = DayHike(
            trail_id=504,
            name="Lake Path",
            distance=Distance(4, "km"),
            elevation_gain_m=0,
            difficulty="easy",
        )
        fake_trail = FakeTrail("Temporary Route", 2.5)

        report = build_trail_report([real_trail, fake_trail])

        self.assertEqual(len(report), 2)
        self.assertIn("Day hike: Lake Path", report[0])
        self.assertIn("Fake trail: Temporary Route", report[1])


if __name__ == "__main__":
    unittest.main()