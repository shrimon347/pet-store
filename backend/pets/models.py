from datetime import date

from django.db import models


# Enum choices for pet_gender
class PetGender(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    UNKNOWN = "UNKNOWN", "Unknown"


# Enum choices for pet_status
class PetStatus(models.TextChoices):
    AVAILABLE = "AVAILABLE", "Available"
    SOLD = "SOLD", "Sold"
    UNDER_TREATMENT = "UNDER_TREATMENT", "Under Treatment"


class Species(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Pet(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="pets")
    age = models.IntegerField()
    breed = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=PetGender.choices, default=PetGender.UNKNOWN)
    status = models.CharField(max_length=20, choices=PetStatus.choices, default=PetStatus.SOLD)
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.name
