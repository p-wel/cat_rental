from django.shortcuts import render
from cats.models import Cat


def index(request):
    return render(request, 'cats/index.html')


def cats_list(request):
    cats = Cat.objects.all()
    context = {'cats_list': cats}
    return render(request, 'cats/list.html', context)


def cat_details(request):
    context = {}
    return render(request, 'cats/details.html', context)


def cat_rented(request):
    context = {}
    return render(request, 'cats/rented.html', context)
