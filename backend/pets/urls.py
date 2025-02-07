"""
    URL Mappings for the petstore
"""

from django.urls import path
from pets.controllers.views import PetDetailAPIView, PetListCreateAPIView

urlpatterns = [
    path("pets/", PetListCreateAPIView.as_view(), name="pets-list-create"),
    path("pets/<int:pet_id>/", PetDetailAPIView.as_view(), name="pets-detail"),
]
