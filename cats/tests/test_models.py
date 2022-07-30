import datetime
from unittest import TestCase

from cats.models import Rental, Cat, Species, Breed
from cats.tests.factories import RentalFactory


class TestModels(TestCase):

    def setUp(self):
        RentalFactory.build_batch(50)

    def test_species_exists(self):
        assert Species.objects.exists()

    def test_breeds_exists(self):
        assert Breed.objects.exists()

    def test_cats_exists(self):
        assert Cat.objects.exists()

    def test_rentals_exists(self):
        assert Rental.objects.exists()

    def test_rental_has_cat(self):
        assert Rental.objects.get(pk=1).cat is not None

    def test_filter_available_between_dates_within_following_month(self):
        """
        Method in filter_available_between_dates() should return Queryset of Cats available in given dates.
        Test checks if cats filtered are not rented between today and tomorrow.
        """
        today = datetime.date.today()
        next_month_day = datetime.date.today() + datetime.timedelta(days=30)

        available_cats = Cat.objects.filter_available_between_dates(today, next_month_day)
        valid_rentals = Rental.objects.filter(
            rental_date__gte=today, return_date__lte=next_month_day
        )

        assert available_cats not in valid_rentals
