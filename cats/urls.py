from django.urls import path
from cats.views import about, index, species_list, cats_list, cat_details, cat_rental_dates, \
    explore_list, handle_cat_rental, congrats_mail

app_name = "cats"

urlpatterns = [
    path('', index, name="index"),
    path('about/', about, name="about"),
    path('species/', species_list, name="species"),
    path('explore/', explore_list, name="explore_list"),
    path('explore/<str:date_from>/<str:date_to>/', explore_list, name="explore_list_dates"),
    path('species/<int:species_id>/', cats_list, name="list"),
    # path('species/<int:species_id>/<str:date_from>/<str:date_to>/', cats_list, name="list_dates"),
    path('cat/<int:cat_id>/', cat_details, name="details"),
    path('cat/<int:cat_id>/rental_dates/', cat_rental_dates, name="rental_dates"),
    path('cat/<int:cat_id>/rental_dates/congrats', congrats_mail, name="congrats_mail"),
    path('cat/<int:cat_id>/rent/', handle_cat_rental, name="rent_the_cat"),
    path('cat/rentals', handle_cat_rental, name="rentals_list"),
]
