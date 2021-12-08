from django.shortcuts import render
from cats.models import Cat


def index(request):
    cats = Cat.objects.all()
    context = {'cats_list': cats}
    return render(request, 'cats/index.html', context)


def cats_list(request):
    cats = Cat.objects.all()
    context = {'cats_list': cats}
    return render(request, 'cats/list.html', context)


def cat_details(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    context = {"cat": cat}
    return render(request, 'cats/details.html', context)


def cat_rented(request):
    return render(request, 'cats/rented.html')

def cats_about(request):
    return render(request, 'cats/about.html')
