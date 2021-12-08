from django.urls import path
from cats.views import cat_details, cats_about, cats_list, index

app_name = "cats"
urlpatterns = [
    # path('cats/<int:cats_id>/rented/', cat_rented, name="rented"),
    path('cats/<int:cat_id>/', cat_details, name="details"),
    path('cats/about', cats_about, name="about"),
    path('cats/', cats_list, name="list"),
    path('', index, name="index"),
]


