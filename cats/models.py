"""
Models used in app
"""
import datetime

from django.core.exceptions import ValidationError
from django.db import models

STATUS_CHOICES = [
    ('0', 'No status'),
    ('1', 'Pending'),
    ('2', 'Actual'),
    ('3', 'Finished'),
    ('4', 'Cancelled'),
]


class TimeStamped(models.Model):
    """TimeStamp using when creating new object"""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CatQuerySet(models.QuerySet):
    def filter_by_dates(self, rental_date, return_date):
        """
        Own method in QuerySet to filter out cats rented in given dates.

        Returns a list of cats available between given dates.
        """
        rentals_list = Rental.objects.filter(
            rental_date__gte=rental_date,
            return_date__lte=return_date
        )
        rented_cats_id_list = rentals_list.values_list("cat")
        available_cats = self.exclude(id__in=rented_cats_id_list)
        return available_cats


class Cat(TimeStamped):
    """Basic class for Cat objects"""
    name = models.CharField(max_length=50)
    breed = models.ForeignKey('cats.Breed', on_delete=models.CASCADE)
    description = models.TextField(default=None, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    objects = CatQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class Breed(models.Model):
    """Basic class for Breed objects"""
    name = models.CharField(max_length=50)
    description = models.TextField(default=None, blank=True)
    species = models.ForeignKey('cats.Species', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Species(models.Model):
    """Basic class for Species objects"""
    name = models.CharField(max_length=50)
    description = models.TextField(default=None, blank=True)

    class Meta:
        verbose_name_plural = "Species"

    def __str__(self):
        return f"{self.name}"


class Rental(models.Model):
    """Basic class for Rental objects"""
    cat = models.ForeignKey("Cat", on_delete=models.CASCADE, related_name="rentals")
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="rentals")
    rental_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='0')

    def clean(self):
        super().clean()
        if self.rental_date < datetime.date.today():
            raise ValidationError("Cannot pick date from the past")
        if self.rental_date > self.return_date:
            raise ValidationError("'Return date' must be further than 'return from'")

        # Check if cat isn't already rented in given dates
        if not Cat.objects.filter_by_dates(self.rental_date, self.return_date).filter(pk=self.cat.pk).exists():
            raise ValidationError("Cat isn't available in given timeframes")

    def __str__(self):
        return f"Rental {self.id} ({self.cat.name})"
