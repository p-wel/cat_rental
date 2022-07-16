import datetime

import factory
from faker import Factory

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        django_get_or_create = ("email",)

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@p-wel_cat_rental.pl")
    password = "password123"


class SpeciesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "cats.Species"

    name = factory.Sequence(lambda n: f"Species_{n}")
    description = factory.Sequence(lambda n: f"Species_description_{n}")


class BreedFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "cats.Breed"

    name = factory.Sequence(lambda n: f"Breed_{n}")
    description = factory.Sequence(lambda n: f"Breed_description_{n}")
    species = factory.SubFactory(SpeciesFactory)


class CatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "cats.Cat"

    name = factory.Sequence(lambda n: f"Cat_{n}")
    breed = factory.SubFactory(BreedFactory)
    description = factory.Sequence(lambda n: f"Cat_description_{n}")


class RentalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "cats.Rental"

    cat = factory.SubFactory(CatFactory)
    user = factory.SubFactory(UserFactory)
    rental_date = factory.Sequence(lambda n: datetime.date.today() + datetime.timedelta(days=n))
    return_date = factory.Sequence(lambda n: datetime.date.today() + datetime.timedelta(days=2 * n))
    status = 2
