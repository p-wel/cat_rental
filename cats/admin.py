"""
Admin for CRUD on objects creating in app
"""
from django.contrib import admin

from .models import Cat, Species, Breed, Rental


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    """Register admin for Cats"""
    list_display = ["id", "name", "breed"]
    search_fields = ["id", "breed"]


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    """Register admin for Species"""
    list_display = ["id", "name"]
    search_fields = ["id", "name"]


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    """Register admin for Breeds"""
    list_display = ["id", "name", "species"]
    search_fields = ["id", "name"]
    list_filter = ["species"]


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    """Register admin for Rentals"""
    list_display = ["id", "user", "cat", "rental_date", "return_date", "valid"]
    list_filter = ["rental_date", "return_date", "valid"]
