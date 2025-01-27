from django.test import TestCase
from pets.models import Pet, PetGender, PetStatus, Species
from pets.serializers import PetSerializer
from rest_framework import serializers


class PetSerializerTests(TestCase):
    def setUp(self):
        """Initialize test data"""
        self.dog_species = Species.objects.create(name="Dog")
        self.cat_species = Species.objects.create(name="Cat")
        self.valid_data = {
            "name": "Buddy",
            "species": self.dog_species.id,
            "age": 5,
            "breed": "Labrador",
            "gender": PetGender.MALE.value,
            "status": PetStatus.AVAILABLE.value,
        }

    def test_valid_serializer_data(self):
        """Test serializer with completely valid data"""
        serializer = PetSerializer(data=self.valid_data)
        print(serializer.is_valid())
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_name_empty(self):
        data = self.valid_data.copy()  # Make a copy to avoid modifying original
        data["name"] = ""
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(str(serializer.errors["name"][0]), "This field may not be blank.")

    def test_name_too_short(self):
        data = self.valid_data.copy()
        data["name"] = "A"
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["name"][0]),
            "Pet name must be at least 2 characters long.",
        )

    def test_age_non_integer(self):
        data = self.valid_data.copy()
        data["age"] = "five"
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["age"][0]), "A valid integer is required."
        )

    def test_age_zero(self):
        data = self.valid_data.copy()
        data["age"] = 0
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["age"][0]), "Age must be a positive number."
        )

    def test_breed_validation(self):
        data = self.valid_data.copy()
        data["breed"] = "A"
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["breed"][0]),
            "Breed must be at least 2 characters long.",
        )

    def test_species_breed_validation(self):
        data = self.valid_data.copy()
        data["breed"] = "Siamese"  # Cat breed with dog species
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            str(serializer.errors["non_field_errors"][0]),
            f"Breed Siamese does not match species Dog",
        )
