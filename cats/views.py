"""
Views used in cat app
"""

import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView

from cats.forms import RentalForm, SearchForm
from cats.models import Cat, Species, Breed, Rental


class IndexView(TemplateView):
    """Simple index view"""

    template_name = "cats/index.html"


class AboutView(TemplateView):
    """Simple about view"""

    template_name = "cats/about.html"


class SpeciesListView(ListView):
    """View to choose a Species"""

    model = Species
    template_name = "cats/species.html"


def explore_list(request):
    """Lists Cats from all kinds of Species"""
    cats = None
    page_obj = None
    search_form = SearchForm(request.GET or None)

    """
    If form is valid, show list.
    If form is not valid, SearchForm will show proper hint
    """
    if search_form.is_valid():
        date_from = search_form.cleaned_data["date_from"]
        date_to = search_form.cleaned_data["date_to"]
        cats = Cat.objects.get_available_cats(date_from, date_to)

        paginator = Paginator(cats, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    context = {"cats_list": cats, "search_form": search_form, "page_obj": page_obj}
    return render(request, "cats/explore_list.html", context)


def cats_list(request, species_id):
    """Lists Cats from only one Species"""
    cats = None
    page_obj = None
    search_form = SearchForm(request.GET or None)
    breeds = Breed.objects.all()

    # If such species id do not exists, then make species=None (html will show proper hint then)
    try:
        species = Species.objects.get(id=species_id)
    except Species.DoesNotExist:
        species = None

    # If form is valid, show list. If not, SearchForm will show proper hint
    if search_form.is_valid():
        date_from = search_form.cleaned_data["date_from"]
        date_to = search_form.cleaned_data["date_to"]
        species_cats = Cat.objects.filter(breed__species=species_id)
        cats = species_cats.get_available_cats(date_from, date_to)

        paginator = Paginator(cats, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    context = {
        "cats_list": cats,
        "breeds_list": breeds,
        "species_id": species_id,
        "search_form": search_form,
        "species": species,
        "page_obj": page_obj,
    }
    return render(request, "cats/cats_list.html", context)


class CatDetailView(DetailView):
    """Detail view for a Cat"""

    model = Cat
    template_name = "cats/details.html"


@login_required
def rental_dates(request, cat_id):
    """
    View to let user Rent a Cat, picking proper dates from a RentalForm.

    - On success redirects to "congrats_mail" view.
    - On failure (If Cat isn't available in given dates) renders "rental_dates" view again.

    Picked dates are validated below, but the clean method (dates logic check and availability check)
    is directly in Rental model (works every time, even from admin).
    """
    cat = get_object_or_404(Cat, pk=cat_id)
    rental_form = RentalForm(
        initial={"cat": cat, "user": request.user}, data=request.POST or None
    )

    # POST means, that user are using the form
    if request.POST:
        if rental_form.is_valid():
            rental_form.save()
            return redirect(reverse("cats:congrats_mail", args=[cat_id]))

    context = {"cat": cat, "rental_form": rental_form}
    return render(request, "cats/rental_dates.html", context)


@login_required
def rentals_history(request):
    """View to show all user's rentals"""
    user_rentals = Rental.objects.filter(user=request.user).order_by("-rental_date")
    today = datetime.date.today()

    paginator = Paginator(user_rentals, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"user_rentals": user_rentals, "today": today, "page_obj": page_obj}

    return render(request, "cats/rentals_history.html", context)


@login_required
def congrats_mail(request, cat_id):
    """View to send confirmation mail to the user and show him congrats info"""
    cat = get_object_or_404(Cat, pk=cat_id)
    congrats_template = render_to_string(
        "cats/congrats_mail_template.html", {"cat": cat}
    )

    send_mail(
        "Congrats, cat rented!",
        congrats_template,
        "",
        [request.user.email],
        fail_silently=False,
    )

    return render(request, "cats/congrats.html", {"cat": cat})
