from django.contrib import admin

from .models import Cat, Species, Breed, Rental


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "breed", "available"]
    search_fields = ["id", "breed"]
    list_filter = ["available"]


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "cat", "rental_date", "return_date"]
    list_filter = ["rental_date", "return_date"]
