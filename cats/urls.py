from django.urls import path
from cats.views import show_cats

urlpatterns = [
    path('', show_cats),
]