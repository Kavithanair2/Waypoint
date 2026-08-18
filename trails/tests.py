from django.test import TestCase
from django.urls import reverse

from .models import Park, Trail


class TrailViewTests(TestCase):

    def setUp(self):
        self.park = Park.objects.create(
            name="Test Park",
            region="Ontario",
        )

        Trail.objects.create(
            name="Long Open Trail",
            park=self.park,
            distance_km=10.0,
            elevation_gain=300,
            difficulty="moderate",
            is_open=True,
        )

        Trail.objects.create(
            name="Closed Trail",
            park=self.park,
            distance_km=2.0,
            elevation_gain=100,
            difficulty="easy",
            is_open=False,
        )

        Trail.objects.create(
            name="Short Open Trail",
            park=self.park,
            distance_km=5.0,
            elevation_gain=150,
            difficulty="easy",
            is_open=True,
        )

    def test_catalog_shows_only_open_trails_in_distance_order(self):
        response = self.client.get(reverse("trail_catalog"))

        self.assertEqual(response.status_code, 200)

        trails = list(response.context["trails"])

        self.assertEqual(
            [trail.name for trail in trails],
            ["Short Open Trail", "Long Open Trail"],
        )

    def test_missing_trail_detail_returns_404(self):
        response = self.client.get(
            reverse("trail_detail", args=[9999])
        )

        self.assertEqual(response.status_code, 404)
