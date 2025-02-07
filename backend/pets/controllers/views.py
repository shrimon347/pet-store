from pets.serializers import PetSerializer
from pets.services.petServices import PetService
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from pets.filters import PetFilter


class PetListCreateAPIView(APIView):
    """
    API View for listing all pets and creating a new pet.
    """

    def get(self, request):
        """
        Retrieve all pets using the PetService layer.
        """
        try:
            pets = PetService.get_all_pets().order_by('id')

             # Apply filters using the FilterSet
            pet_filter = PetFilter(request.GET, queryset=pets)
            filtered_pets = pet_filter.qs

            paginator = PageNumberPagination()
            paginator.page_size = 10 # adjust if need more object per view

            #paginate the queryset
            result_page = paginator.paginate_queryset(filtered_pets, request)

            #serlize the paginated reults
            serializer = PetSerializer(result_page, many=True)
            #return the paginated response
            # return Response({"pets": serializer.data}, status=status.HTTP_200_OK)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        Create a new pet using the PetService layer.
        """
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Extract validated data and delegate creation to PetService
                pet =serializer.save()
                return Response(PetSerializer(pet).data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PetDetailAPIView(APIView):
    """
    API View for retrieving, updating, and deleting a specific pet.
    """

    def get(self, request, pet_id):
        """
        Retrieve a pet by ID using the PetService layer.
        """
        try:
            pet = PetService.get_pet_by_id(pet_id)
            if not pet:
                return Response(
                    {"error": f"Pet with ID {pet_id} does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = PetSerializer(pet)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pet_id):
        """
        Update an existing pet using the PetService layer.
        """
        try:
            pet = PetService.get_pet_by_id(pet_id)
            if not pet:
                return Response(
                    {"error": f"Pet with ID {pet_id} does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = PetSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                # Delegate update to PetService
                updated_pet = PetService.update_pet(
                    pet_id=pet_id,
                    name=serializer.validated_data.get("name"),
                    species=serializer.validated_data.get("species"),
                    age=serializer.validated_data.get("age"),
                    breed=serializer.validated_data.get("breed"),
                    gender=serializer.validated_data.get("gender"),
                    status=serializer.validated_data.get("status"),
                )
                return Response(
                    PetSerializer(updated_pet).data, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pet_id):
        """
        Delete a pet by ID using the PetService layer.
        """
        try:
            success = PetService.delete_pet(pet_id)
            if success:
                return Response(
                    {"message": "Pet deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT,
                )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
