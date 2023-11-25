# cake_server/urls.py

from django.urls import path

from .views import CakeDetailView, CakeListView

urlpatterns = [
    path("cakes/", CakeListView.as_view(), name="cake-list"),
    path("cakes/<int:cake_id>/", CakeDetailView.as_view(), name="cake-detail"),
]
