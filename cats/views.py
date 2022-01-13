from django.shortcuts import render
from cats.models import Cat, Species, Breed


def index(request):
    return render(request, 'cats/index.html')


def species_list(request):
    species = Species.objects.all()
    context = {'species_list': species}
    return render(request, 'cats/species.html', context)


def cats_list(request, species_id):
    breeds = Breed.objects.all()
    cats = Cat.objects.all()
    species = species_id
    context = {'breeds_list': breeds, 'cats_list': cats, 'species_id': species}
    return render(request, 'cats/cats_list.html', context)


def explore_list(request):
    cats = Cat.objects.all()
    context = {'all_cats': cats}
    return render(request, 'cats/explore_list.html', context)


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
