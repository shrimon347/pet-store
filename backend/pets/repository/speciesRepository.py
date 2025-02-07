from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist
from pets.models import Species


class SpeciesRepository:
    """Repository layer for handling species model database operations."""

    @staticmethod
    def get_all_species() -> List[Species]:
        """Retrieve all species from the database."""
        return list(Species.objects.all())

    @staticmethod
    def get_species_by_id(species_id: int) -> Optional[Species]:
        """Retrieve a species by ID."""
        try:
            return Species.objects.get(id=species_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_species_by_name(species: str) -> Optional[Species]:
        """Retrieve a species by name."""
        try:
            return Species.objects.get(name=species)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_species(name: str) -> Species:
        """Create and return a new species."""
        return Species.objects.create(name=name)

    @staticmethod
    def update_species(species: Species, name: str) -> Species:
        """Update an existing species."""
        species.name = name
        species.save()
        return species

    @staticmethod
    def delete_species(species: Species) -> None:
        """Delete a species from the database."""
        species.delete()
