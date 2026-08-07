"""Unit tests for Waypoint mixins and method-resolution order."""

import unittest

from waypoint_core.distance import Distance
from waypoint_core.mixins import PermitRequiredMixin, SeasonalAccessMixin
from waypoint_core.trail import Trail
from waypoint_core.trail_types import DayHike, ManagedDayHike


class MixinTests(unittest.TestCase):
    """Test mixin composition and predictable method resolution."""

    def test_managed_day_hike_uses_both_mixins(self) -> None:
        trail = ManagedDayHike(
            trail_id=401,
            name="Alpine Reserve",
            distance=Distance(6, "km"),
            elevation_gain_m=300,
            difficulty="moderate",
        )

        summary = trail.summary()

        self.assertIn("Day hike: Alpine Reserve", summary)
        self.assertIn("permit required", summary)
        self.assertIn("seasonal access", summary)

    def test_mixins_preserve_day_hike_behaviour(self) -> None:
        trail = ManagedDayHike(
            trail_id=402,
            name="Protected Valley",
            distance=Distance(8, "km"),
            elevation_gain_m=600,
            difficulty="hard",
        )

        self.assertAlmostEqual(trail.estimated_time(), 3.0)
        self.assertIsInstance(trail, DayHike)
        self.assertIsInstance(trail, Trail)

    def test_managed_day_hike_has_predictable_mro(self) -> None:
        mro = ManagedDayHike.mro()

        self.assertLess(
            mro.index(SeasonalAccessMixin),
            mro.index(PermitRequiredMixin),
        )
        self.assertLess(
            mro.index(PermitRequiredMixin),
            mro.index(DayHike),
        )

    def test_mro_contains_expected_classes(self) -> None:
        class_names = [
            class_type.__name__
            for class_type in ManagedDayHike.mro()
        ]

        self.assertEqual(
            class_names[:6],
            [
                "ManagedDayHike",
                "SeasonalAccessMixin",
                "PermitRequiredMixin",
                "DayHike",
                "Trail",
                "ABC",
            ],
        )


if __name__ == "__main__":
    unittest.main()