from typing import List, Optional

from pets.models import Pet
from pets.repository.petRepository import PetRepository


class PetService:
    """Service layer for handling business login related to pets."""

    @staticmethod
    def get_all_pets() -> List[Pet]:
        """Retrive all pets."""
        return PetRepository.get_all_pets()

    @staticmethod
    def get_pet_by_id(pet_id: int) -> Optional[Pet]:
        """Retrive a pet by ID."""
        return PetRepository.get_pet_by_id(pet_id)

    @staticmethod
    def create_pet(pet_data: dict) -> Optional[Pet]:
        """Create a new pet after validating species."""
        return PetRepository.create_pet(pet_data)

    @staticmethod
    def update_pet(pet: Pet, updated_data: dict) -> Optional[Pet]:
        """Update an existing pet after validating species."""
        pet = PetRepository.get_pet_by_id(pet.id)

        if not pet:
            return None
        return PetRepository.update_pet(pet, updated_data)

    @staticmethod
    def delete_pet(pet_id: int) -> None:
        """Delete a pet by ID."""
        pet = PetRepository.get_pet_by_id(pet_id)

        if not pet:
            return False
        PetRepository.delete_pet(pet)
        return True
