from django.urls import path
from cats.views import cats_about, index, species_list, cats_list, cat_details, cat_rental_dates, cat_rented, \
    explore_list, handle_cat_rental

app_name = "cats"
urlpatterns = [
    path('cat/<int:cat_id>/rented/', cat_rented, name="rented"),
    path('cat/<int:cat_id>/rental_dates/', cat_rental_dates, name="rental_dates"),

    path('cat/<int:cat_id>/rentals', handle_cat_rental, name="rent_the_cat"),
    path('cat/rentals', handle_cat_rental, name="rentals_list"),
    path('cat/<int:cat_id>/', cat_details, name="details"),

    path('species/<int:species_id>/', cats_list, name="list"),
    path('species/', species_list, name="species"),
    path('explore/', explore_list, name="explore_list"),
    path('about', cats_about, name="about"),
    path('', index, name="index"),
]
