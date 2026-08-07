"""Unit tests for the Waypoint Trail abstract base class."""

import unittest

from waypoint_core.distance import Distance
from waypoint_core.trail import Trail
from waypoint_core.trail_types import DayHike


class TrailTests(unittest.TestCase):
    """Test Trail validation, equality, class state, and abstraction."""

    def setUp(self) -> None:
        """Reset shared class state before every test."""
        Trail.set_default_unit("km")

    def test_from_dict_populates_trail_correctly(self) -> None:
        trail = DayHike.from_dict(
            {
                "id": 101,
                "name": "Maple Lookout",
                "distance": 8.4,
                "unit": "km",
                "elevation_gain_m": 310,
                "difficulty": "moderate",
            }
        )

        self.assertEqual(trail.trail_id, 101)
        self.assertEqual(trail.name, "Maple Lookout")
        self.assertEqual(trail.distance.magnitude, 8.4)
        self.assertEqual(trail.distance.unit, "km")
        self.assertEqual(trail.elevation_gain_m, 310.0)
        self.assertEqual(trail.difficulty, "moderate")

    def test_invalid_difficulty_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            DayHike(
                trail_id=102,
                name="Granite Pass",
                distance=Distance(12, "km"),
                elevation_gain_m=540,
                difficulty="impossible",
            )

    def test_set_difficulty_validates_new_value(self) -> None:
        trail = DayHike(
            trail_id=103,
            name="Cedar Boardwalk",
            distance=Distance(3, "km"),
            elevation_gain_m=20,
            difficulty="easy",
        )

        trail.set_difficulty("hard")

        self.assertEqual(trail.difficulty, "hard")

        with self.assertRaises(ValueError):
            trail.set_difficulty("extreme")

    def test_trails_with_same_id_compare_equal(self) -> None:
        first = DayHike(
            trail_id=104,
            name="Pine Creek",
            distance=Distance(4, "km"),
            elevation_gain_m=80,
            difficulty="easy",
        )

        second = DayHike(
            trail_id=104,
            name="Different Trail Name",
            distance=Distance(20, "mi"),
            elevation_gain_m=900,
            difficulty="expert",
        )

        self.assertEqual(first, second)

    def test_trails_with_different_ids_do_not_compare_equal(self) -> None:
        first = DayHike(
            trail_id=105,
            name="River Bend",
            distance=Distance(5, "km"),
            elevation_gain_m=90,
            difficulty="easy",
        )

        second = DayHike(
            trail_id=106,
            name="River Bend",
            distance=Distance(5, "km"),
            elevation_gain_m=90,
            difficulty="easy",
        )

        self.assertNotEqual(first, second)

    def test_default_unit_affects_future_trails_only(self) -> None:
        first = DayHike.from_dict(
            {
                "id": 107,
                "name": "Aspen Walk",
                "distance": 3,
                "elevation_gain_m": 25,
                "difficulty": "easy",
            }
        )

        Trail.set_default_unit("mi")

        second = DayHike.from_dict(
            {
                "id": 108,
                "name": "Lake Ridge",
                "distance": 3,
                "elevation_gain_m": 100,
                "difficulty": "moderate",
            }
        )

        self.assertEqual(first.distance.unit, "km")
        self.assertEqual(second.distance.unit, "mi")

    def test_missing_dictionary_field_raises_value_error(self) -> None:
        incomplete_data = {
            "id": 109,
            "name": "Summit Path",
            "distance": 7,
            "difficulty": "hard",
        }

        with self.assertRaises(ValueError):
            DayHike.from_dict(incomplete_data)

    def test_trail_cannot_be_instantiated_directly(self) -> None:
        with self.assertRaises(TypeError):
            Trail(
                trail_id=110,
                name="Abstract Trail",
                distance=Distance(5, "km"),
                elevation_gain_m=100,
                difficulty="easy",
            )

    def test_incomplete_subclass_cannot_be_instantiated(self) -> None:
        class IncompleteTrail(Trail):
            def estimated_time(self) -> float:
                return 1.0

        with self.assertRaises(TypeError):
            IncompleteTrail(
                trail_id=111,
                name="Incomplete Trail",
                distance=Distance(5, "km"),
                elevation_gain_m=100,
                difficulty="easy",
            )


if __name__ == "__main__":
    unittest.main()
