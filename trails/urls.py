from django.urls import path

from . import views


urlpatterns = [
    path("", views.catalog, name="trail_catalog"),
    path("<int:trail_id>/", views.detail, name="trail_detail"),
]
