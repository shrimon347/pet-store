from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist
from pets.models import Pet, Species


class PetRepository:
    """Repository layer for handling pet model datanase operations."""

    @staticmethod
    def get_all_pets() -> List[Pet]:
        """Retrive all pets from the database."""
        return Pet.objects.all()

    @staticmethod
    def get_pet_by_id(pet_id: int) -> Optional[Pet]:
        """Retrive a pet by ID"""
        try:
            return Pet.objects.get(id=pet_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_pet(pet_data: dict) -> Optional[Pet]:
        """Create and reaturn a new pet, ensuring species is valid."""
        species_id = pet_data.get("species")
        try:
            pet_data["species"] = Species.objects.get(id=species_id)
            return Pet.objects.create(**pet_data)
        except Species.DoesNotExist:
            return None

    @staticmethod
    def update_pet(pet: Pet, updated_data: dict) -> Optional[Pet]:
        """Update an existing pet, ensuring species is valid if being updated"""
        if "species" in updated_data:
            species_id = updated_data.get("species")
            try:
                updated_data["species"] = Species.objects.get(id=species_id)
            except Species.DoesNotExist:
                return None
        for key, value in updated_data.items():
            setattr(pet, key, value)
        pet.save()
        return pet

    @staticmethod
    def delete_pet(pet: Pet) -> None:
        """Delete a pet from the database."""
        pet.delete()
