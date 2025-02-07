from django.test import TestCase
from pets.models import Pet, PetGender, PetStatus, Species
from pets.serializers import PetSerializer


class PetSerializerTests(TestCase):
    def setUp(self):
        self.species = Species.objects.create(name="Dog")
        self.pet_data = {
            "name": "Buddy",
            "species": "Dog",  # Use "species" instead of "species"
            "age": 2,
            "breed": "Golden Retriever",
            "gender": PetGender.MALE,
            "status": PetStatus.AVAILABLE,
        }
        self.pet = Pet.objects.create(
            name="Buddy",
            species=self.species,
            age=2,
            breed="Golden Retriever",
            gender=PetGender.MALE,
            status=PetStatus.AVAILABLE,
        )

    def test_valid_serializer(self):
        serializer = PetSerializer(instance=self.pet)
        self.assertEqual(
            serializer.data,
            {
                "id": self.pet.id,
                "name": "Buddy",
                "species": "Dog",  # Expect "species" in the serialized output
                "age": 2,
                "breed": "Golden Retriever",
                "gender": "MALE",
                "status": "AVAILABLE",
            },
        )

    def test_invalid_name(self):
        data = self.pet_data.copy()
        data["name"] = ""
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_invalid_age(self):
        data = self.pet_data.copy()
        data["age"] = -1
        serializer = PetSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("age", serializer.errors)

    def test_create_pet_with_valid_data(self):
        serializer = PetSerializer(data=self.pet_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        pet = serializer.save()
        self.assertEqual(pet.name, "Buddy")
        self.assertEqual(pet.species.name, "Dog")

    def test_update_pet_species(self):
        new_species = Species.objects.create(name="Cat")
        data = {"species": "Cat"}  # Update species using "species"
        serializer = PetSerializer(instance=self.pet, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_pet = serializer.save()
        self.assertEqual(updated_pet.species.name, "Cat")
