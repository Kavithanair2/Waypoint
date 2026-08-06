"""
Unit tests for Distance validation, conversion, and operators.
"""

import unittest

from waypoint_core.distance import Distance


class DistanceTests(unittest.TestCase):
    """Test Distance validation, conversion, operators, and properties."""

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

    def test_same_unit_addition(self) -> None:
        result = Distance(3, "km") + Distance(2, "km")

        self.assertEqual(result, Distance(5, "km"))
        self.assertEqual(result.unit, "km")

    def test_mixed_unit_addition_returns_left_unit(self) -> None:
        result = Distance(1, "mi") + Distance(1.609344, "km")

        self.assertAlmostEqual(result.magnitude, 2.0, places=9)
        self.assertEqual(result.unit, "mi")

    def test_same_unit_subtraction(self) -> None:
        result = Distance(5, "km") - Distance(2, "km")

        self.assertEqual(result, Distance(3, "km"))

    def test_subtraction_rejects_negative_result(self) -> None:
        with self.assertRaises(ValueError):
            Distance(2, "km") - Distance(3, "km")

    def test_equal_distances_with_different_units_compare_equal(self) -> None:
        self.assertEqual(
            Distance(1, "mi"),
            Distance(1.609344, "km"),
        )

    def test_distances_support_less_than_and_greater_than(self) -> None:
        self.assertLess(Distance(1, "km"), Distance(1, "mi"))
        self.assertGreater(Distance(2, "mi"), Distance(3, "km"))

    def test_distances_can_be_sorted(self) -> None:
        distances = [
            Distance(5, "km"),
            Distance(1, "mi"),
            Distance(2, "km"),
        ]

        sorted_distances = sorted(distances)

        self.assertEqual(
            sorted_distances,
            [
                Distance(1, "mi"),
                Distance(2, "km"),
                Distance(5, "km"),
            ],
        )

    def test_string_representation(self) -> None:
        self.assertEqual(str(Distance(5, "km")), "5 km")

    def test_developer_representation(self) -> None:
        self.assertEqual(
            repr(Distance(5, "km")),
            "Distance(magnitude=5.0, unit='km')",
        )


if __name__ == "__main__":
    unittest.main()
