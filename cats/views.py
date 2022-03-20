import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView

from cats.forms import RentalForm, SearchForm
from cats.models import Cat, Species, Breed, Rental


class IndexView(TemplateView):
    template_name = 'cats/index.html'


class AboutView(TemplateView):
    template_name = 'cats/about.html'


class SpeciesListView(ListView):
    model = Species
    template_name = 'cats/species.html'


def explore_list(request):
    cats = None
    search_form = SearchForm(request.GET or None)

    if search_form.is_valid():
        date_from = search_form.cleaned_data['date_from']
        date_to = search_form.cleaned_data['date_to']
        cats = Cat.objects.filter_by_dates(date_from, date_to)

    context = {'cats_list': cats, 'search_form': search_form}
    return render(request, 'cats/explore_list.html', context)


def cats_list(request, species_id):
    cats = None
    search_form = SearchForm(request.GET or None)
    breeds = Breed.objects.all()

    try:
        Species.objects.filter(id=species_id).get()
    except Species.DoesNotExist:
        species_exists = False
        context = {'species_exists': species_exists}
        return render(request, 'cats/cats_list.html', context)

    if search_form.is_valid():
        date_from = search_form.cleaned_data['date_from']
        date_to = search_form.cleaned_data['date_to']
        cats = Cat.objects.filter_by_dates(date_from, date_to)
        search_form.helper.form_action = reverse("cats:cats_list", args=[species_id])
    context = {'cats_list': cats, 'breeds_list': breeds, 'species_id': species_id, 'search_form': search_form}

    return render(request, 'cats/cats_list.html', context)


class CatDetailView(DetailView):
    model = Cat
    template_name = 'cats/details.html'


@login_required
def rental_dates(request, cat_id, available=True):
    cat = get_object_or_404(Cat, pk=cat_id)
    rental_form = RentalForm()
    context = {"cat": cat, "rental_form": rental_form, "available": available}

    return render(request, 'cats/rental_dates.html', context)


@login_required
def handle_rent(request, cat_id=None):
    user = request.user
    rent_from = request.POST.get("date_from")
    rent_to = request.POST.get("date_to")

    try:
        cat = Cat.objects.filter_by_dates(rent_from, rent_to).get(pk=cat_id)
        Rental.objects.create(
            user=user,
            cat=cat,
            rental_date=rent_from,
            return_date=rent_to,
            valid=True
        )
        cat.save()
        return congrats_mail(request, cat_id)

    except Cat.DoesNotExist:
        available = False
        return rental_dates(request, cat_id, available)


@login_required
def rentals_history(request):
    user_rentals = Rental.objects.filter(user=request.user).order_by('-rental_date')
    today = datetime.date.today()

    return render(request, "cats/rentals_history.html", {'user_rentals': user_rentals, 'today': today})


@login_required
def congrats_mail(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    congrats_template = render_to_string('cats/congrats_mail_template.html', {'cat': cat})

    send_mail('Congrats, cat rented!',
              congrats_template,
              '',
              [request.user.email],
              fail_silently=False)

    return render(request, 'cats/congrats.html', {'cat': cat})
