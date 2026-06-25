from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("download/", views.download_leads, name="download_leads"),
    path("areas/", views.areas_for_city, name="areas_for_city"),  # legacy stub
]
