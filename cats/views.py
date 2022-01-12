from django.shortcuts import render
from cats.models import Cat, Species, Breed


def index(request):
    return render(request, 'cats/index.html')


def species_list(request):
    species = Species.objects.all()
    context = {'species_list': species}
    return render(request, 'cats/species.html', context)


def breeds_list(request, breed_id):
    breed = Breed.objects.get(pk=breed_id)
    context = {'breed': breed}
    return render(request, 'cats/breeds.html', context)


def cats_list(request, breed_id):
    breeds = Breed.objects.get(pk=breed_id)
    cats = Cat.objects.all()
    context = {'breeds_list': breeds, 'cats_list': cats}
    return render(request, 'cats/cats_list.html', context)


def all_cats_list(request):
    cats = Cat.objects.all()
    context = {'all_cats': cats}
    return render(request, 'cats/cats_list_all.html', context)


def cat_details(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    context = {"cat": cat}
    return render(request, 'cats/details.html', context)


def cat_rental_dates(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    context = {"cat": cat}
    return render(request, 'cats/rental_dates.html', context)


def cat_rented(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    context = {"cat": cat}
    return render(request, 'cats/rented.html', context)


def cats_about(request):
    return render(request, 'cats/about.html')
