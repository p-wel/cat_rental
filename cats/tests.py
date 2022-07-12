"""
Unit tests for the app
"""
import datetime

from cats.models import Cat
from cats.models import Rental


def test_filter_by_dates(self):
    """
    filter_by_dates() should return Queryset of Cats available in given dates.
    Test checks if cats filtered are not rented in those dates.
    """
    today = datetime.date.today()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    if Cat.objects.all().exists():
        available_cats = Cat.objects.filter_available_between_dates(today, tomorrow)
        valid_rentals = Rental.objects.filter(
            rental_date__gte=today, return_date__lte=tomorrow
        )
        assert available_cats not in valid_rentals
    else:
        assert AssertionError("No objects to check in given dates")
