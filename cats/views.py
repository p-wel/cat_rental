import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
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
def cat_rental_dates(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    rental_form = RentalForm()
    context = {"cat": cat, "rental_form": rental_form}
    return render(request, 'cats/rental_dates.html', context)


@login_required
def handle_cat_rental(request, cat_id=None):
    user = request.user

    def handle_rent():
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
            print("WOLNY")
            return congrats_mail(request, cat_id)
        except Cat.DoesNotExist:
            # TODO: Show error msg:
            print('Cat not available in given timeframes')
            return cat_rental_dates(request, cat_id)

    def handle_return(rental_id):
        keys = [
            key for key in request.POST.keys()
            if key.startswith("cat_")
        ]
        key = int(keys[0].split("_")[1])
        """
        keys - taking out proper cat's id from submit button in:
                /rentals_history.html
                    button name="cat_{{ rental.cat.id }}"
        """
        cat = Cat.objects.get(pk=key)

        # TODO: last() should be changed for this rental's id
        # TODO: also, it should make Rental.valid = False

        rental = Rental.objects.filter(user=user, cat=cat).last()
        """
        rental - last rental of given cat, rented by given user
        last() method to avoid assigning older rentals that weren't signed as returned before
        """
        rental.return_date = timezone.now()
        rental.valid = False
        rental.save()

        # TODO TRY TO TAKE RENTAL ID FROM THE BUTTON, SET THIS RENTAL'S RETURN DATE TO NOW AND VALID=FALSE, THEN SAVE:
        rental = Rental.objects.get(pk=rental_id)
        rental.return_date = timezone.now()
        rental.valid = False
        rental.save()

        # """
        # if not - to avoid double saves if user would click a button more than once
        #         or if user would refresh/has connection issues
        # """
        return HttpResponseRedirect(reverse("cats:rentals_history"))

    if user.is_authenticated:
        if request.GET.get("rent"):
            return handle_rent()
        else:
            return handle_return()

    # rentals = Rental.objects.filter(user=user)
    # return render(request, "cats/rentals_history.html", {'rentals': rentals})


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
