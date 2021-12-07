from django.contrib.auth.models import User
from django.db import models


class Cat(models.Model):
    species = models.CharField(max_length=50)
    # species: House Cat, Farm Cat, Feral Cat

    breed = models.CharField(max_length=50)
    # House cat: American Curl, Sphinx, Ragamuffin, Siberian Cat, Persian Cat
    # Farm cat: Sheep's Cat, Barn Cat
    # Feral cat: Bengal Tiger, Lion, Cheetah, Jaguar, Leopard

    description = models.TextField(default=None, blank=True)
    available = models.BooleanField(default=True)
    last_rental_date = models.DateTimeField(default=None, blank=True, null=True)
    last_return_date = models.DateTimeField(default=None, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

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