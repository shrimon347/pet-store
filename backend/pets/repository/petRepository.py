from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist
from pets.models import Pet, PetGender, PetStatus
from pets.repository.speciesRepository import SpeciesRepository


class PetRepository:
    """Repository layer for handling pet model database operations."""

    @staticmethod
    def get_all_pets():
        """
        Retrieve all pets from the database.
        """
        return Pet.objects.all()

    @staticmethod
    def get_pet_by_id(pet_id: int) -> Optional[Pet]:
        """
        Retrieve a pet by ID.
        Returns None if the pet does not exist.
        """
        try:
            return Pet.objects.get(id=pet_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_pet(
        name: str,
        species: str,
        age: int,
        breed: str,
        gender: str,
        status: str,
    ) -> Pet:
        """
        Create and return a new pet.
        If the species does not exist, it will be created dynamically.
        Validates gender and status using the enums.
        """
        # Validate gender and status using the enums
        if gender not in PetGender.values:
            raise ValueError(f"Invalid gender: {gender}")
        if status not in PetStatus.values:
            raise ValueError(f"Invalid status: {status}")

        # Use the SpeciesRepository to handle species creation or retrieval
        species = SpeciesRepository.get_species_by_name(species)
        if not species:
            species = SpeciesRepository.create_species(name=species)

        # Create the pet
        return Pet.objects.create(
            name=name,
            species=species,
            age=age,
            breed=breed,
            gender=gender,
            status=status,
        )

    @staticmethod
    def update_pet(
        pet: Pet,
        name: Optional[str] = None,
        species: Optional[str] = None,
        age: Optional[int] = None,
        breed: Optional[str] = None,
        gender: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Pet:
        """
        Update an existing pet.
        If the species does not exist, it will be created dynamically.
        Validates gender and status using the enums.
        """
        if name is not None:
            pet.name = name
        if species is not None:
            # Use the SpeciesRepository to handle species creation or retrieval
            species = SpeciesRepository.get_species_by_name(species)
            if not species:
                species = SpeciesRepository.create_species(name=species)
            pet.species = species
        if age is not None:
            pet.age = age
        if breed is not None:
            pet.breed = breed
        if gender is not None:
            if gender not in PetGender.values:
                raise ValueError(f"Invalid gender: {gender}")
            pet.gender = gender
        if status is not None:
            if status not in PetStatus.values:
                raise ValueError(f"Invalid status: {status}")
            pet.status = status
        pet.save()
        return pet

    @staticmethod
    def delete_pet(pet: Pet) -> None:
        """
        Delete a pet from the database.
        """
        pet.delete()
