from rest_framework import serializers

from .models import Pet, Species


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ["id", "name"]


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
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("Pet name cannot contain numbers.")
        return value

    def validate_species(self, value):
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
        import re

        if not re.match(r"^[a-zA-Z\s]+$", value):
            raise serializers.ValidationError(
                "Breed can only contain letters and spaces."
            )
        return value

    def validate(self, data):
        """
        Cross-field validation for species and breed compatibility.
        """
        species = data.get("species")
        breed = data.get("breed")

        # Hardcoded species-to-breed mapping for validation
        known_breed_species_mapping = {
            "Dog": ["Labrador", "German Shepherd", "Poodle"],
            "Cat": ["Siamese", "Persian", "Maine Coon"],
        }

        # Get the species name
        species_name = species.name if isinstance(species, Species) else None

        # Validate species and breed compatibility
        if species_name and breed:
            if species_name not in known_breed_species_mapping:
                raise serializers.ValidationError(
                    {"non_field_errors": f"Unknown species: {species_name}"}
                )

            if breed not in known_breed_species_mapping[species_name]:
                raise serializers.ValidationError(
                    {
                        "non_field_errors": f"Breed {breed} does not match species {species_name}"
                    }
                )

        return data
