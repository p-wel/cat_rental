from django.contrib.auth.models import User
from django.db import models


class Species(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(default=None, blank=True)
    """
    Species:
    - House Cat
    - Farm Cat
    - Feral Cat
    """

    def __str__(self):
        return f"{self.name}"


class Cat(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)

    """
    Breeds:
    - House cat: American Curl, Sphinx, Ragamuffin, Siberian Cat, Persian Cat
    - Farm cat: Sheep's Cat, Barn Cat
    - Feral cat: Bengal Tiger, Lion, Cheetah, Jaguar, Leopard
    """

    description = models.TextField(default=None, blank=True)
    available = models.BooleanField(default=True)
    last_rental_date = models.DateTimeField(default=None, blank=True, null=True)
    last_return_date = models.DateTimeField(default=None, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    species = models.ForeignKey("cats.Species", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}. {self.breed}"

    def rent(self):
        self.available = False


class Customer(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Rental(Customer):
    rental_customer = Customer.name

    def __str__(self):
        return f"Rental order: {self.id} - Customer: {self.rental_customer}"
