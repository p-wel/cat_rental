"""
Admin for CRUD on objects creating in app
"""
from django.contrib import admin

from .models import Cat, Species, Breed, Rental


@admin.action(description='Status 0: no status yet')
def update_status_to_no_status(request, queryset):
    queryset.update(status=0)


@admin.action(description='Status 1: Pending')
def update_status_to_pending(request, queryset):
    queryset.update(status=1)


@admin.action(description='Status 2: Actual')
def update_status_to_actual(request, queryset):
    queryset.update(status=2)


@admin.action(description='Status 3: Finished')
def update_status_to_finished(request, queryset):
    queryset.update(status=3)


@admin.action(description='Status 4: Cancelled')
def update_status_to_cancelled(request, queryset):
    queryset.update(status=4)


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
    list_display = ["id", "user", "cat", "rental_date", "return_date", "status"]
    list_filter = ["status", "rental_date", "return_date"]
    search_fields = ["id", "cat__name", "user__username"]
    actions = [update_status_to_no_status,
               update_status_to_pending,
               update_status_to_actual,
               update_status_to_finished,
               update_status_to_cancelled]
