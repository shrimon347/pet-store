from rest_framework import serializers
from .models import Pet, Species


class PetSerializer(serializers.ModelSerializer):
    species = serializers.PrimaryKeyRelatedField(queryset=Species.objects.all())

    class Meta:
        model = Pet
        fields = ["id", "name", "species", "age", "breed", "gender", "status"]

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value) < 2:
            raise serializers.ValidationError(
                "Pet name must be at least 2 characters long."
            )
        if len(value) > 255:
            raise serializers.ValidationError("Pet name cannot exceed 255 characters.")
        
        # Allow spaces and hyphens in pet names
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Pet name cannot contain numbers.")
        
        return value

    def validate_species(self, value):
        """Validate species."""
        if not value:
            raise serializers.ValidationError("Species is required.")
        return value

    def validate_age(self, value):
        if value is None:
            raise serializers.ValidationError("Age cannot be empty.")
        if not isinstance(value, int):
            raise serializers.ValidationError("Age must be an integer.")
        if value <= 0:
            raise serializers.ValidationError("Age must be a positive number.")
        if value > 30:
            raise serializers.ValidationError("Maximum pet age is 30 years.")
        return value

    def validate_breed(self, value):
        if not value:
            raise serializers.ValidationError("Breed cannot be empty.")
        if len(value) < 2:
            raise serializers.ValidationError(
                "Breed must be at least 2 characters long."
            )
        if len(value) > 255:
            raise serializers.ValidationError("Breed cannot exceed 255 characters.")
        
        # Allow letters, spaces, hyphens, and apostrophes
        import re
        if not re.match(r"^[a-zA-Z\s\-']+$", value):
            raise serializers.ValidationError(
                "Breed can only contain letters, spaces, hyphens, and apostrophes."
            )
        return value