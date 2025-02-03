import re

from pets.models import Pet, PetGender, PetStatus, Species
from rest_framework import serializers


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"


class PetSerializer(serializers.ModelSerializer):

    species = serializers.CharField(required=True)

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "species",
            "age",
            "breed",
            "gender",
            "status",
        ]

    def validate_name(self, value):
        """
        Ensure name is not empty and contains only alphabetic characters (and optionally spaces).
        """
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        if not re.match(r"^[A-Za-z\s]+$", value):
            raise serializers.ValidationError(
                "Name can only contain letters and spaces."
            )
        return value

    def validate_species(self, value):
        """
        Custom validation to ensure species is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Species name cannot be empty.")
        return value

    def validate_age(self, value):
        """Ensure age is a positive integer."""
        if value <= 0:
            raise serializers.ValidationError("Age must be a positive integer.")
        return value

    def create(self, validated_data):
        """Handle species assignment during pet creation."""
        species = validated_data.pop("species")  # Extract species
        species, _ = Species.objects.get_or_create(
            name=species
        )  # Get or create species
        validated_data["species"] = species
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Handle species updates properly."""
        species = validated_data.pop("species", None)
        if species:
            species = Species.objects.filter(name=species).first()
            if not species:
                raise serializers.ValidationError({"species": "Invalid species name."})
            validated_data["species"] = species
        return super().update(instance, validated_data)
