from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class CheckAddDateMixin:
    def added_earlier_than_n_days(self, n=1):
        """Chceck if cat was added earlier than now() - days"""
        delta = timedelta(days=n)
        return now() - self.created > delta


class TimeStamped(models.Model, CheckAddDateMixin):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CatQuerySet(models.QuerySet):

    def filter_by_dates(self, rental_date, return_date):
        rentals_list = Rental.objects.filter(rental_date__gte=rental_date, return_date__lte=return_date)
        rented_cats_id_list = rentals_list.values_list("cat")
        available_cats = self.exclude(id__in=rented_cats_id_list)
        return available_cats


class Cat(TimeStamped):
    name = models.CharField(max_length=50)
    breed = models.ForeignKey('cats.Breed', on_delete=models.CASCADE)
    objects = CatQuerySet.as_manager()

    """
    <Species: Breeds>
    - House cat: American Curl, Sphinx, Ragamuffin, Siberian Cat, Persian Cat
    - Farm cat: Sheep's Cat, Barn Cat
    - Feral cat: Bengal Tiger, Lion, Cheetah, Jaguar, Leopard
    """

    description = models.TextField(default=None, blank=True)
    available = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    user = models.ManyToManyField("auth.User", blank=True)

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class Breed(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default=None, blank=True)
    species = models.ForeignKey('cats.Species', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Species(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default=None, blank=True)

    class Meta:
        verbose_name_plural = "Species"

    def __str__(self):
        return f"{self.name}"


class Rental(models.Model):
    cat = models.ForeignKey("Cat", on_delete=models.CASCADE, related_name="rentals")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="rentals")
    rental_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Rental {self.id} ({self.cat.name})"
