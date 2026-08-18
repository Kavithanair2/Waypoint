from django.urls import path

from . import views


urlpatterns = [
    path("", views.catalog, name="trail_catalog"),
    path("<int:trail_id>/", views.detail, name="trail_detail"),
    path("parks/<int:park_id>/", views.park_detail, name="park_detail"),
]
