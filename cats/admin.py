from django.contrib import admin
from .models import Cat, Species


@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ["id", "species", "breed", "last_rental_date", "last_return_date", "available"]
    search_fields = ["id", "species", "breed"]
    list_filter = ["species", "available"]


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]
