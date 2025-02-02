from django.test import TestCase
from pets.models import Pet, PetGender, PetStatus, Species
from pets.serializers import PetSerializer


class PetSerializerTests(TestCase):
    def setUp(self):
        """Initialize test data"""
        # Creating species for testing
        self.dog_species = Species.objects.create(name="Dog")
        self.cat_species = Species.objects.create(name="Cat")

        # Pass only the ID of species (no full object)
        self.valid_data = {
            "name": "Buddy",
            "species": self.cat_species.id,  # Pass the species id only
            "age": 5,
            "breed": "Labrador",
            "gender": PetGender.MALE.value,
            "status": PetStatus.AVAILABLE.value,
        }

    def test_valid_serializer_data(self):
        """Test serializer with completely valid data"""
        serializer = PetSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_name_empty(self):
        """Test that name cannot be empty"""
        data = self.valid_data.copy()  # Make a copy to avoid modifying original
        data["name"] = ""
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["name"][0]), "This field may not be blank."
        )

    def test_name_too_short(self):
        """Test that name must be at least 2 characters long"""
        data = self.valid_data.copy()
        data["name"] = "A"
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["name"][0]),
            "Pet name must be at least 2 characters long.",
        )

    def test_age_non_integer(self):
        """Test that age must be an integer"""
        data = self.valid_data.copy()
        data["age"] = "five"
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["age"][0]), "A valid integer is required."
        )

    def test_age_zero(self):
        """Test that age must be greater than 0"""
        data = self.valid_data.copy()
        data["age"] = 0
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["age"][0]), "Age must be a positive number."
        )

    def test_breed_validation(self):
        """Test that breed must be at least 2 characters long"""
        data = self.valid_data.copy()
        data["breed"] = "A"
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["breed"][0]),
            "Breed must be at least 2 characters long.",
        )
