from django.urls import path
from cats.views import cats_about, index, species_list, cats_list, cat_details, cat_rental_dates, cat_rented, \
    breeds_list

app_name = "cats"
urlpatterns = [
    path('cat/<int:cat_id>/rented/', cat_rented, name="rented"),
    path('cat/<int:cat_id>/rental_dates/', cat_rental_dates, name="rental_dates"),
    path('cat/<int:cat_id>/', cat_details, name="details"),
    path('species/<int:breed_id>/', cats_list, name="list"),
    # TODO i breads.html wypełnić po zrobieniu routingu
    path('species/<int:species_id>/', breeds_list, name="breeds"),
    path('species/', species_list, name="species"),
    path('about', cats_about, name="about"),
    path('', index, name="index"),
]


