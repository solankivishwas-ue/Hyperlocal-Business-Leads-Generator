from __future__ import annotations

from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("download/", views.download_csv, name="download_csv"),
]
