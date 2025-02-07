from unittest import TestCase
from unittest.mock import patch

from pets.models import Pet, PetGender, PetStatus, Species
from pets.repository.petRepository import PetRepository
from pets.repository.speciesRepository import SpeciesRepository
from pets.services.petServices import PetService


class PetServiceTests(TestCase):
    def setUp(self):
        """Initialize test data before each test."""
        self.species = Species(id=1, name="Dog")
        self.pet = Pet(
            id=1,
            name="Buddy",
            species=self.species,
            age=5,
            breed="Labrador",
            gender=PetGender.MALE.value,
            status=PetStatus.AVAILABLE.value,
        )

    @patch.object(PetRepository, "get_all_pets", return_value=[])
    def test_get_all_pets(self, mock_get_all_pets):
        """Test retrieving all pets."""
        pets = PetService.get_all_pets()
        self.assertEqual(pets, [])
        mock_get_all_pets.assert_called_once()

    @patch.object(PetRepository, "get_pet_by_id", return_value=None)
    def test_get_pet_by_id_not_found(self, mock_get_pet_by_id):
        """Test retrieving a pet by ID that does not exist."""
        pet = PetService.get_pet_by_id(99)
        self.assertIsNone(pet)
        mock_get_pet_by_id.assert_called_once_with(99)

    @patch.object(PetRepository, "create_pet")
    def test_create_pet(self, mock_create_pet):
        """Test creating a pet."""
        mock_create_pet.return_value = self.pet
        created_pet = PetService.create_pet(
            name="Buddy",
            species="Dog",
            age=5,
            breed="Labrador",
            gender=PetGender.MALE.value,
            status=PetStatus.AVAILABLE.value,
        )
        self.assertEqual(created_pet, self.pet)
        mock_create_pet.assert_called_once()

    @patch.object(PetRepository, "get_pet_by_id", return_value=None)
    def test_update_pet_not_found(self, mock_get_pet_by_id):
        """Test updating a pet that does not exist."""
        with self.assertRaises(ValueError) as context:
            PetService.update_pet(99, name="New Name")
        self.assertEqual(str(context.exception), "Pet with ID 99 does not exist.")

    @patch.object(PetRepository, "delete_pet")
    @patch.object(PetRepository, "get_pet_by_id", return_value=None)
    def test_delete_pet_not_found(self, mock_get_pet_by_id, mock_delete_pet):
        """Test deleting a pet that does not exist."""
        with self.assertRaises(ValueError) as context:
            PetService.delete_pet(99)
        self.assertEqual(str(context.exception), "Pet with ID 99 does not exist.")
        mock_get_pet_by_id.assert_called_once()
        mock_delete_pet.assert_not_called()

    @patch.object(SpeciesRepository, "get_species_by_name", return_value=None)
    @patch.object(PetRepository, "get_all_pets", return_value=[])
    def test_get_pets_by_species_not_found(
        self, mock_get_all_pets, mock_get_species_by_name
    ):
        """Test retrieving pets by species when the species does not exist."""
        pets = PetService.get_pets_by_species("Unknown")
        self.assertEqual(pets, [])
        mock_get_species_by_name.assert_called_once_with("Unknown")

    @patch.object(PetRepository, "get_all_pets", return_value=[])
    def test_get_pets_by_status_invalid(self, mock_get_all_pets):
        """Test retrieving pets by an invalid status."""
        with self.assertRaises(ValueError) as context:
            PetService.get_pets_by_status("INVALID_STATUS")
        self.assertEqual(str(context.exception), "Invalid status: INVALID_STATUS")
