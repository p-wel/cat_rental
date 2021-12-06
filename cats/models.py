from django.db import models


class Cat(models.Model):
    # species: house cat, farm cat, feral cat
    species = models.CharField(max_length=255)
    # House cat: American curl, Sphinx, Ragamuffin, Siberian cat, Persian Cat
    # Farm cat: Ship's cat, Barn cat
    # Feral cat: Bengal tiger, Lion, Cheetah, Jaguar, Leopard
    breed = models.CharField(max_length=255)
