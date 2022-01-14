from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import admin
from django.forms import forms

from .models import Cat, Species, Breed


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