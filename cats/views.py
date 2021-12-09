from django.shortcuts import render
from cats.models import Cat, Species


def index(request):
    return render(request, 'cats/index.html')


def species_list(request):
    species = Species.objects.all()
    context = {'species_list': species}
    return render(request, 'cats/species.html', context)


def cats_list(request, species_id):
    species = Species.objects.get(pk=species_id)
    cats = Cat.objects.all()
    context = {'species': species, 'cats_list': cats}
    return render(request, 'cats/cats.html', context)


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
