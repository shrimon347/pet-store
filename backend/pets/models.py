from django.db import models
from datetime import date

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
    name = models.CharField(max_length=255, unique=True)
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Pet(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name="pets")
    birthday = models.DateField()
    breed = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=PetGender.choices, default=PetGender.UNKNOWN
    )
    status = models.CharField(
        max_length=20, choices=PetStatus.choices, default=PetStatus.AVAILABLE
    )
    version = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    @property
    def age(self):
        """
        Calculate the pet's age in years or months (if under 1 year).
        """
        today = date.today()
        age_years = today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )
        if age_years > 0:
            return f"{age_years} year(s)"
        else:
            age_months = (today.year - self.birthday.year) * 12 + today.month - self.birthday.month
            return f"{age_months} month(s)"
