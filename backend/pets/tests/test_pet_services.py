from unittest.mock import MagicMock, patch

from django.test import TestCase
from pets.models import Pet, PetGender, PetStatus, Species
from pets.services.petServices import PetService


class PetServiceTestCase(TestCase):
    """Test cases for the PetService class."""

    def setUp(self):
        """Set up test data."""
        self.species = Species(id=1, name="Dog")
        self.pet_data = {
            "id": 1,
            "name": "Charlie",
            "species": self.species,
            "age": 4,
            "breed": "Poodle",
            "gender": PetGender.MALE,
            "status": PetStatus.AVAILABLE,
        }
        self.pet = Pet(**self.pet_data)

    @patch("pets.repository.petRepository.PetRepository.get_all_pets")
    def test_get_all_pets(self, mock_get_all_pets):
        """Test retrieving all pets."""
        mock_get_all_pets.return_value = [self.pet]

        pets = PetService.get_all_pets()
        self.assertEqual(len(pets), 1)
        self.assertEqual(pets[0].name, "Charlie")
        mock_get_all_pets.assert_called_once()

    @patch("pets.repository.petRepository.PetRepository.get_pet_by_id")
    def test_get_pet_by_id_valid(self, mock_get_pet_by_id):
        """Test retrieving a pet by valid ID."""
        mock_get_pet_by_id.return_value = self.pet

        pet = PetService.get_pet_by_id(1)
        self.assertIsNotNone(pet)
        self.assertEqual(pet.name, "Charlie")
        mock_get_pet_by_id.assert_called_once_with(1)

    @patch("pets.repository.petRepository.PetRepository.get_pet_by_id")
    def test_get_pet_by_id_invalid(self, mock_get_pet_by_id):
        """Test retrieving a pet by invalid ID (returns None)."""
        mock_get_pet_by_id.return_value = None

        pet = PetService.get_pet_by_id(99)
        self.assertIsNone(pet)
        mock_get_pet_by_id.assert_called_once_with(99)

    @patch("pets.repository.petRepository.PetRepository.create_pet")
    def test_create_pet(self, mock_create_pet):
        """Test creating a new pet."""
        mock_create_pet.return_value = self.pet

        pet = PetService.create_pet(self.pet_data)
        self.assertIsNotNone(pet)
        self.assertEqual(pet.name, "Charlie")
        mock_create_pet.assert_called_once_with(self.pet_data)

    @patch("pets.repository.petRepository.PetRepository.get_pet_by_id")
    @patch("pets.repository.petRepository.PetRepository.update_pet")
    def test_update_pet_valid(self, mock_update_pet, mock_get_pet_by_id):
        """Test updating an existing pet."""
        updated_data = {"name": "Max", "age": 5}
        mock_get_pet_by_id.return_value = self.pet
        mock_update_pet.return_value = Pet(**{**self.pet_data, **updated_data})

        pet = PetService.update_pet(self.pet, updated_data)
        self.assertIsNotNone(pet)
        self.assertEqual(pet.name, "Max")
        self.assertEqual(pet.age, 5)
        mock_get_pet_by_id.assert_called_once_with(self.pet.id)
        mock_update_pet.assert_called_once_with(self.pet, updated_data)

    @patch("pets.repository.petRepository.PetRepository.get_pet_by_id")
    @patch("pets.repository.petRepository.PetRepository.update_pet")
    def test_update_pet_invalid(self, mock_update_pet, mock_get_pet_by_id):
        """Test updating a pet that does not exist (should return None)."""
        mock_get_pet_by_id.return_value = None

        pet = PetService.update_pet(self.pet, {"name": "Max"})
        self.assertIsNone(pet)
        mock_get_pet_by_id.assert_called_once_with(self.pet.id)
        mock_update_pet.assert_not_called()

    @patch("pets.repository.petRepository.PetRepository.get_pet_by_id")
    @patch("pets.repository.petRepository.PetRepository.delete_pet")
    def test_delete_pet_valid(self, mock_delete_pet, mock_get_pet_by_id):
        """Test deleting a valid pet."""
        mock_get_pet_by_id.return_value = self.pet

        result = PetService.delete_pet(1)
        self.assertTrue(result)
        mock_get_pet_by_id.assert_called_once_with(1)
        mock_delete_pet.assert_called_once_with(self.pet)

    @patch("pets.repository.petRepository.PetRepository.get_pet_by_id")
    @patch("pets.repository.petRepository.PetRepository.delete_pet")
    def test_delete_pet_invalid(self, mock_delete_pet, mock_get_pet_by_id):
        """Test deleting a pet that does not exist (should return False)."""
        mock_get_pet_by_id.return_value = None

        result = PetService.delete_pet(99)
        self.assertFalse(result)
        mock_get_pet_by_id.assert_called_once_with(99)
        mock_delete_pet.assert_not_called()
