from pets.models import Species
from pets.serializers import PetSerializer
from pets.services.petServices import PetService, SpeciesService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PetListCreateAPIView(APIView):
    """API View for listing and creating pets."""

    def get(self, request):
        """Retrieve all pets."""
        pets = PetService.get_all_pets()
        serializer = PetSerializer(pets, many=True)
        return Response({"pets": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """Create a new pet."""
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Create the pet using the service layer
                pet = PetService.create_pet(serializer.validated_data)
                if not pet:
                    return Response(
                        {"error": "Failed to create pet."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Return the serialized pet data
                response = PetSerializer(pet).data
                return Response(response, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Log the exception and return a meaningful error message
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PetDetailAPIView(APIView):
    """API View for retrieving, updating, and deleting a pet."""

    def get(self, request, pet_id):
        """Retrieve a single pet."""
        pet = PetService.get_pet_by_id(pet_id)
        if not pet:
            return Response(
                {"error": "Pet not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(PetSerializer(pet).data, status=status.HTTP_200_OK)

    def put(self, request, pet_id):
        """Update an existing pet."""
        pet = PetService.get_pet_by_id(pet_id)
        if not pet:
            return Response(
                {"error": "Pet not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                # Update the pet using the service layer
                updated_pet = PetService.update_pet(pet_id, serializer.validated_data)
                if not updated_pet:
                    return Response(
                        {"error": "Invalid species."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                return Response(
                    PetSerializer(updated_pet).data, status=status.HTTP_200_OK
                )

            except Exception as e:
                # Log the exception and return a meaningful error message
                return Response(
                    {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pet_id):
        """Delete a pet."""
        success = PetService.delete_pet(pet_id)
        if not success:
            return Response(
                {"error": "Pet not found."}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"message": "Pet deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
