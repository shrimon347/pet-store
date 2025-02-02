from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist
from pets.models import Pet, Species


class SpeciesRepository:
    """Repository layer for handling species model database operations."""

    @staticmethod
    def get_all_species() -> List[Species]:
        """Retrieve all species from the database."""
        return Species.objects.all()

    @staticmethod
    def get_species_by_id(species_id: int) -> Optional[Species]:
        """Retrieve a species by ID."""
        try:
            return Species.objects.get(id=species_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_species(species_data: dict) -> Species:
        """Create and return a new species."""
        return Species.objects.create(**species_data)

    @staticmethod
    def update_species(species: Species, updated_data: dict) -> Species:
        """Update an existing species."""
        for key, value in updated_data.items():
            setattr(species, key, value)
        species.save()
        return species

    @staticmethod
    def delete_species(species: Species) -> None:
        """Delete a species from the database."""
        species.delete()


class PetRepository:
    """Repository layer for handling pet model database operations."""

    @staticmethod
    def get_all_pets() -> List[Pet]:
        """Retrieve all pets from the database."""
        return Pet.objects.all()

    @staticmethod
    def get_pet_by_id(pet_id: int) -> Optional[Pet]:
        """Retrieve a pet by ID."""
        try:
            return Pet.objects.get(id=pet_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_pet(pet_data: dict) -> Optional[Pet]:
        """Create and return a new pet."""
        species = pet_data.get("species")
        
        # Ensure species is a valid Species object
        if not isinstance(species, Species):
            raise ValueError("Invalid species.")
        
        # Create the pet
        return Pet.objects.create(**pet_data)

    @staticmethod
    def update_pet(pet: Pet, updated_data: dict) -> Optional[Pet]:
        """Update an existing pet."""
        if "species" in updated_data:
            species = updated_data.get("species")
        
        # Ensure species is a valid Species object
        if not isinstance(species, Species):
            raise ValueError("Invalid species.")
        
        updated_data["species"] = species
    
        # Update other fields
        for key, value in updated_data.items():
            setattr(pet, key, value)
    
        pet.save()
        return pet

    @staticmethod
    def delete_pet(pet: Pet) -> None:
        """Delete a pet from the database."""
        pet.delete()
