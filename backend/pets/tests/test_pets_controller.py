from django.urls import reverse
from pets.models import Pet, PetGender, PetStatus, Species
from pets.services.petServices import PetService
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class PetAPITestCase(APITestCase):
    def setUp(self):
        """
        Set up initial data for testing.
        """
        self.client = APIClient()
        self.species = Species.objects.create(name="Dog")
        self.pet_data = {
            "name": "Buddy",
            "species": "Dog",
            "age": 3,
            "breed": "Golden Retriever",
            "gender": PetGender.MALE,
            "status": PetStatus.AVAILABLE,
        }
        self.pet = Pet.objects.create(
            name="Buddy",
            species=self.species,
            age=3,
            breed="Golden Retriever",
            gender=PetGender.MALE,
            status=PetStatus.AVAILABLE,
        )

    def test_get_all_pets(self):
        """
        Test retrieving all pets via GET /pets/.
        """
        url = reverse("pets-list-create")  # Updated to match the URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Buddy")

    def test_create_pet_success(self):
        """
        Test creating a new pet via POST /pets/.
        """
        url = reverse("pets-list-create")  # Updated to match the URL name
        new_pet_data = {
            "name": "Max",
            "species": "Cat",
            "age": 2,
            "breed": "Siamese",
            "gender": PetGender.FEMALE,
            "status": PetStatus.SOLD,
        }
        response = self.client.post(url, new_pet_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Max")
        self.assertEqual(response.data["species"], "Cat")

    def test_create_pet_invalid_data(self):
        """
        Test creating a pet with invalid data.
        """
        url = reverse("pets-list-create")  # Updated to match the URL name
        invalid_pet_data = {
            "name": "",
            "species": "Dog",
            "age": -1,
            "breed": "Golden Retriever",
            "gender": PetGender.MALE,
            "status": PetStatus.AVAILABLE,
        }
        response = self.client.post(url, invalid_pet_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)  # Name cannot be empty
        self.assertIn("age", response.data)  # Age must be positive

    def test_get_pet_by_id_success(self):
        """
        Test retrieving a pet by ID via GET /pets/<pet_id>/.
        """
        url = reverse(
            "pets-detail", kwargs={"pet_id": self.pet.id}
        )  # Updated to match the URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Buddy")
        self.assertEqual(response.data["species"], "Dog")

    def test_get_pet_by_id_not_found(self):
        """
        Test retrieving a pet by ID when the pet does not exist.
        """
        url = reverse(
            "pets-detail", kwargs={"pet_id": 999}
        )  # Updated to match the URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Pet with ID 999 does not exist.")

    def test_update_pet_success(self):
        """
        Test updating an existing pet via PUT /pets/<pet_id>/.
        """
        url = reverse(
            "pets-detail", kwargs={"pet_id": self.pet.id}
        )  # Updated to match the URL name
        updated_data = {
            "name": "Charlie",
            "age": 5,
            "status": PetStatus.SOLD,
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Charlie")
        self.assertEqual(response.data["age"], 5)
        self.assertEqual(response.data["status"], PetStatus.SOLD)

    def test_update_pet_invalid_data(self):
        """
        Test updating a pet with invalid data.
        """
        url = reverse(
            "pets-detail", kwargs={"pet_id": self.pet.id}
        )  # Updated to match the URL name
        invalid_data = {
            "age": -1,
            "status": "INVALID_STATUS",
        }
        response = self.client.put(url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("age", response.data)  # Age must be positive
        self.assertIn("status", response.data)  # Invalid status value

    def test_delete_pet_success(self):
        """
        Test deleting a pet via DELETE /pets/<pet_id>/.
        """
        url = reverse(
            "pets-detail", kwargs={"pet_id": self.pet.id}
        )  # Updated to match the URL name
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pet.objects.count(), 0)

    def test_delete_pet_not_found(self):
        """
        Test deleting a pet when the pet does not exist.
        """
        url = reverse(
            "pets-detail", kwargs={"pet_id": 999}
        )  # Updated to match the URL name
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Pet with ID 999 does not exist.")
