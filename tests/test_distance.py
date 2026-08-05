"""
Unit tests for the Waypoint Distance value type.
"""

import unittest

from waypoint_core.distance import Distance


class DistanceTests(unittest.TestCase):
    """Test validation, conversion, and read-only Distance properties."""

    def test_negative_magnitude_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Distance(-1, "km")


    def test_invalid_unit_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            Distance(5, "metres")

    def test_conversion_round_trip_returns_original_value(self) -> None:
        original = Distance(10, "km")
        round_trip = original.convert("mi").convert("km")

        self.assertAlmostEqual(
            round_trip.magnitude,
            original.magnitude,
            places=9,
        )
        self.assertEqual(round_trip.unit, "km")


    def test_magnitude_and_unit_are_read_only(self) -> None:
        distance = Distance(5, "km")

        with self.assertRaises(AttributeError):
            distance.magnitude = 8

        with self.assertRaises(AttributeError):
            distance.unit = "mi"



if __name__ == "__main__":
    unittest.main()