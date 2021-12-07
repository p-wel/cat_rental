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
        return f"ID: {self.id}. {self.breed} ({self.species})"
