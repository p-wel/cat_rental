from django.contrib import admin
from .models import Cat

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ["id", "species", "breed", "last_rental_date", "last_return_date", "available"]
    search_fields = ["id", "speecies", "breed"]
    list_filter = ["species", "breed", "available"]