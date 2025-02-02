from typing import List, Optional

from pets.models import Pet, Species
from pets.repository.petRepository import PetRepository, SpeciesRepository


class SpeciesService:
    """Service layer for handling business logic related to species."""

    @staticmethod
    def get_all_species() -> List[Species]:
        """Retrieve all species."""
        return SpeciesRepository.get_all_species()

    @staticmethod
    def get_species_by_id(species_id: int) -> Optional[Species]:
        """Retrieve a species by ID."""
        return SpeciesRepository.get_species_by_id(species_id)

    @staticmethod
    def create_species(species_data: dict) -> Species:
        """Create a new species."""
        # Assuming species_data is a dict with 'id' and 'name'
        return SpeciesRepository.create_species(species_data)

    @staticmethod
    def update_species(species_id: int, updated_data: dict) -> Optional[Species]:
        """Update an existing species."""
        species = SpeciesRepository.get_species_by_id(species_id)
        if not species:
            return None
        return SpeciesRepository.update_species(species, updated_data)

    @staticmethod
    def delete_species(species_id: int) -> bool:
        """Delete a species by ID."""
        species = SpeciesRepository.get_species_by_id(species_id)
        if not species:
            return False
        SpeciesRepository.delete_species(species)
        return True


class PetService:
    """Service layer for handling business logic related to pets."""

    @staticmethod
    def get_all_pets() -> List[Pet]:
        """Retrieve all pets."""
        return PetRepository.get_all_pets()

    @staticmethod
    def get_pet_by_id(pet_id: int) -> Optional[Pet]:
        """Retrieve a pet by ID."""
        return PetRepository.get_pet_by_id(pet_id)

    @staticmethod
    def create_pet(pet_data: dict) -> Optional[Pet]:
        """Create a new pet after validating species."""
        species = pet_data.get("species")
        
        # Ensure species is a valid Species object
        if not isinstance(species, Species):
            raise ValueError("Invalid species.")
        
        # Create the pet
        return PetRepository.create_pet(pet_data)

    @staticmethod
    def update_pet(pet_id: int, updated_data: dict) -> Optional[Pet]:
        """Update an existing pet after validating species."""
        pet = PetRepository.get_pet_by_id(pet_id)
        if not pet:
            return None
        
        if "species" in updated_data:
            species = updated_data.get("species")
            
            # Ensure species is a valid Species object
            if not isinstance(species, Species):
                raise ValueError("Invalid species.")
            
            updated_data["species"] = species
        
        return PetRepository.update_pet(pet, updated_data)
    @staticmethod
    def delete_pet(pet_id: int) -> bool:
        """Delete a pet by ID."""
        pet = PetRepository.get_pet_by_id(pet_id)

        if not pet:
            return False
        PetRepository.delete_pet(pet)
        return True
