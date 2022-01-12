from django.contrib import admin

from main.models import Order
from .models import Cat, Species, Breed


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ["id", "breed", "last_rental_date", "last_return_date", "available"]
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


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
    # list_display = ["user", "cat"]
