from django.urls import path
from cats.views import cats_list, \
    handle_cat_rental, congrats_mail, IndexView, CatDetailView, RentalCreateView, AboutView, \
    SpeciesListView, CatsListView, cat_rental_dates, explore_list

app_name = "cats"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('about/', AboutView.as_view(), name="about"),
    path('species/', SpeciesListView.as_view(), name="species"),
    path('explore/', explore_list, name="explore_list"),
    path('species/<int:species_id>/', cats_list, name="list"),
    path('cat/<int:pk>/', CatDetailView.as_view(), name="details"),
    path('cat/<int:cat_id>/rental_dates/', cat_rental_dates, name="rental_dates"),
    path('cat/<int:cat_id>/rental_dates/congrats', congrats_mail, name="congrats_mail"),
    path('cat/<int:cat_id>/rent/', handle_cat_rental, name="rent_the_cat"),
    path('cat/rentals', handle_cat_rental, name="rentals_list"),
]
