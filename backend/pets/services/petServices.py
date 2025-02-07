
from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist
from pets.models import Pet, PetGender, PetStatus, Species
from pets.repository.petRepository import PetRepository
from pets.repository.speciesRepository import SpeciesRepository


class PetService:
    """
    Service layer for handling business logic related to pets.
    All methods are static to avoid dependency on instance attributes.
    """

    @staticmethod
    def get_all_pets() -> List[Pet]:
        """
        Retrieve all pets from the database.
        """
        return PetRepository.get_all_pets()

    @staticmethod
    def get_pet_by_id(pet_id: int) -> Optional[Pet]:
        """
        Retrieve a pet by ID.
        Returns None if the pet does not exist.
        """
        return PetRepository.get_pet_by_id(pet_id)

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
        Create a new pet.
        - Validates input data.
        - Ensures species exists or creates it dynamically.
        - Applies business rules before saving the pet.
        """
        # Validate age (example business rule: age must be positive)
        if age <= 0:
            raise ValueError("Age must be a positive integer.")

        # Validate breed (example business rule: breed cannot be empty)
        if not breed.strip():
            raise ValueError("Breed cannot be empty.")

        print(f"Creating pet with species: {species}")
        # Validate species (ensure it's not empty or None)
        if not species or not species.strip():
            raise ValueError("Species name cannot be empty.")

        # Ensure species exists or create it dynamically
        species, _ = Species.objects.get_or_create(name=species)

        # Delegate creation to the repository
        return PetRepository.create_pet(
            name=name,
            species=species,
            age=age,
            breed=breed,
            gender=gender,
            status=status,
        )

    @staticmethod
    def update_pet(
        pet_id: int,
        name: Optional[str] = None,
        species: Optional[str] = None,
        age: Optional[int] = None,
        breed: Optional[str] = None,
        gender: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[Pet]:
        """
        Update an existing pet.
        - Validates input data.
        - Ensures species exists or creates it dynamically.
        - Applies business rules before updating the pet.
        """
        # Retrieve the pet by ID
        pet = PetRepository.get_pet_by_id(pet_id)
        if not pet:
            raise ValueError(f"Pet with ID {pet_id} does not exist.")

        # Validate age if provided (example business rule: age must be positive)
        if age is not None and age <= 0:
            raise ValueError("Age must be a positive integer.")

        # Validate breed if provided (example business rule: breed cannot be empty)
        if breed is not None and not breed.strip():
            raise ValueError("Breed cannot be empty.")

        # Delegate update to the repository
        return PetRepository.update_pet(
            pet=pet,
            name=name,
            species=species,
            age=age,
            breed=breed,
            gender=gender,
            status=status,
        )

    @staticmethod
    def delete_pet(pet_id: int) -> bool:
        """
        Delete a pet by ID.
        Returns True if deletion is successful, raises ValueError if the pet does not exist.
        """
        pet = PetRepository.get_pet_by_id(pet_id)
        if not pet:
            raise ValueError(f"Pet with ID {pet_id} does not exist.")
        PetRepository.delete_pet(pet)
        return True

    @staticmethod
    def get_pets_by_species(species: str) -> List[Pet]:
        """
        Retrieve all pets of a specific species.
        If the species does not exist, returns an empty list.
        """
        species = SpeciesRepository.get_species_by_name(species)
        if not species:
            return []
        return [pet for pet in PetRepository.get_all_pets() if pet.species == species]

    @staticmethod
    def get_pets_by_status(status: str) -> List[Pet]:
        """
        Retrieve all pets with a specific status.
        Validates the status against the PetStatus enum.
        """
        if status not in PetStatus.values:
            raise ValueError(f"Invalid status: {status}")
        return [pet for pet in PetRepository.get_all_pets() if pet.status == status]
