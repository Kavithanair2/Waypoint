"""Unit tests for the Waypoint Itinerary class."""

import unittest

from waypoint_core.distance import Distance
from waypoint_core.itinerary import Itinerary
from waypoint_core.trail_types import DayHike


class ItineraryTests(unittest.TestCase):
    """Test itinerary composition and total-distance behaviour."""

    def setUp(self) -> None:
        self.first_trail = DayHike(
            trail_id=201,
            name="Aspen Walk",
            distance=Distance(2, "km"),
            elevation_gain_m=20,
            difficulty="easy",
        )

        self.second_trail = DayHike(
            trail_id=202,
            name="Lake Ridge",
            distance=Distance(3.5, "km"),
            elevation_gain_m=140,
            difficulty="moderate",
        )

        self.third_trail = DayHike(
            trail_id=203,
            name="Summit Path",
            distance=Distance(4.5, "km"),
            elevation_gain_m=500,
            difficulty="hard",
        )

    def test_three_trails_report_correct_total_distance(self) -> None:
        itinerary = Itinerary(
            [
                self.first_trail,
                self.second_trail,
                self.third_trail,
            ]
        )

        total = itinerary.total_distance()

        self.assertAlmostEqual(total.magnitude, 10.0)
        self.assertEqual(total.unit, "km")

    def test_adding_to_one_itinerary_does_not_change_another(self) -> None:
        first_itinerary = Itinerary()
        second_itinerary = Itinerary()

        first_itinerary.add_trail(self.first_trail)

        self.assertEqual(len(first_itinerary), 1)
        self.assertEqual(len(second_itinerary), 0)

    def test_trails_remain_in_insertion_order(self) -> None:
        itinerary = Itinerary()

        itinerary.add_trail(self.second_trail)
        itinerary.add_trail(self.first_trail)

        self.assertEqual(
            itinerary.trails,
            (self.second_trail, self.first_trail),
        )

    def test_constructor_copies_supplied_trail_collection(self) -> None:
        source_trails = [self.first_trail]
        itinerary = Itinerary(source_trails)

        source_trails.append(self.second_trail)

        self.assertEqual(len(source_trails), 2)
        self.assertEqual(len(itinerary), 1)

    def test_mixed_units_are_converted_for_total(self) -> None:
        kilometre_trail = DayHike(
            trail_id=204,
            name="Forest Path",
            distance=Distance(1.609344, "km"),
            elevation_gain_m=40,
            difficulty="easy",
        )


        mile_trail = DayHike(
            trail_id=205,
            name="Creek Loop",
            distance=Distance(1, "mi"),
            elevation_gain_m=60,
            difficulty="moderate",
        )

        itinerary = Itinerary([kilometre_trail, mile_trail])
        total = itinerary.total_distance("km")

        self.assertAlmostEqual(total.magnitude, 3.218688, places=6)
        self.assertEqual(total.unit, "km")

    def test_invalid_object_cannot_be_added(self) -> None:
        itinerary = Itinerary()

        with self.assertRaises(TypeError):
            itinerary.add_trail("Not a Trail")

    def test_empty_itinerary_has_zero_kilometres(self) -> None:
        itinerary = Itinerary()

        total = itinerary.total_distance()

        self.assertEqual(total.magnitude, 0.0)
        self.assertEqual(total.unit, "km")



if __name__ == "__main__":
    unittest.main()