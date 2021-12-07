from django.urls import path
from cats.views import *

urlpatterns = [
    path('cats/1/rented/', cat_rented),
    # path('cats/<int:cats_id>/rented/', cat_rented),
    path('cats/1/', cat_details),
    # path('cats/<int:pk>/', cat_details),

    path('cats/', cats_list),
    path('', index),

]


