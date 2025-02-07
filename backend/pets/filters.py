import django_filters
from pets.models import Pet, PetGender, PetStatus


class PetFilter(django_filters.FilterSet):
    """
    FilterSet for the Pet model.
    Allows filtering by species, breed, gender, and status.
    """

    species = django_filters.CharFilter(
        field_name="species__name", lookup_expr="iexact"
    )  # Case-insensitive match on related Species name
    breed = django_filters.CharFilter(
        field_name="breed", lookup_expr="iexact"
    )  # Case-insensitive match
    gender = django_filters.CharFilter(field_name="gender", lookup_expr="iexact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = Pet
        fields = ["species", "breed", "gender", "status"]
