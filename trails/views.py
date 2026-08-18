from django.shortcuts import get_object_or_404, render

from waypoint_core.distance import Distance
from waypoint_core.trail_types import DayHike

from .models import Park, Trail


def catalog(request):
    trails = Trail.objects.filter(is_open=True).order_by("distance_km")

    return render(request, "catalog.html", {"trails": trails})


def detail(request, trail_id):
    trail = get_object_or_404(Trail, id=trail_id)

    domain_trail = DayHike(
        trail_id=trail.id,
        name=trail.name,
        distance=Distance(float(trail.distance_km), "km"),
        elevation_gain_m=trail.elevation_gain,
        difficulty=trail.difficulty,
    )

    estimated_time = domain_trail.estimated_time()

    return render(
        request,
        "trail_detail.html",
        {
            "trail": trail,
            "estimated_time": estimated_time,
        },
    )

def park_detail(request, park_id):
    park = get_object_or_404(Park, id=park_id)
    trails = park.trail_set.all().order_by("distance_km")

    return render(
        request,
        "park_detail.html",
        {
            "park": park,
            "trails": trails,
        },
    )
