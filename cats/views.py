from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from cats.forms import RentalForm, ListForm
from cats.models import Cat, Species, Breed, Rental


def index(request):
    return render(request, 'cats/index.html')


def about(request):
    return render(request, 'cats/about.html')


def explore_list(request):
    cats = Cat.objects.all()
    date_form = ListForm()
    # date_form.helper.form_action = reverse("cats:explore_list_dates")
    context = {'all_cats': cats, 'date_form': date_form}
    return render(request, 'cats/explore_list.html', context)


def species_list(request):
    species = Species.objects.all()
    context = {'species_list': species}
    return render(request, 'cats/species.html', context)


def cats_list(request, species_id):
    cats = Cat.objects.all()
    species = species_id
    breeds = Breed.objects.all()
    date_form = ListForm()
    # date_form.helper.form_action = reverse("cats:list_dates")
    context = {'breeds_list': breeds, 'cats_list': cats, 'species_id': species, 'date_form': date_form}
    return render(request, 'cats/cats_list.html', context)


def cat_details(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    date_form = RentalForm()
    date_form.helper.form_action = reverse("cats:rental_dates", args=[cat_id])
    context = {"cat": cat, "rental_form": date_form}
    return render(request, 'cats/details.html', context)


def congrats_mail(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    congrats_template = render_to_string('cats/congrats_mail_template.html', {'cat': cat})

    send_mail('Congrats, cat rented!',
              congrats_template,
              '',  # TODO put from_mail here
              [request.user.email],
              fail_silently=False)
    return render(request, 'cats/congrats.html', {'cat': cat})


def cat_rental_dates(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    rental_form = RentalForm()
    rental_form.helper.form_action = reverse("cats:rent_the_cat", args=[cat_id])
    context = {"cat": cat, "rental_form": rental_form}
    return render(request, 'cats/rental_dates.html', context)


def handle_cat_rental(request, cat_id=None):
    def handle_rent():
        cat = Cat.objects.get(pk=cat_id)
        if cat.available:
            Rental.objects.create(
                user=user,
                cat=cat,
                rental_date=request.POST.get("date_from"),
                return_date=request.POST.get("date_to")
            )
            cat.available = False
            cat.save()
        return HttpResponseRedirect(reverse("cats:details", args=[cat_id]))

    def handle_return():
        keys = [
            key for key in request.POST.keys()
            if key.startswith("cat_")
        ]
        key = int(keys[0].split("_")[1])
        """
        keys - taking out proper cat's id from submit button in:
                /rentals_list.html
                    button name="cat_{{ rental.cat.id }}
        """
        cat = Cat.objects.get(pk=key)
        rental = Rental.objects.filter(user=user, cat=cat).last()
        """
        rental - last rental of given cat, rented by given user
        last() method to avoid assigning older rentals that weren't signed as returned before
        """

        rental.return_date = timezone.now()
        rental.save()
        cat.available = True
        cat.save()

        """
        if not - to avoid double saves if user would click a button more than once
                or if user would refresh/has connection issues
        """
        return HttpResponseRedirect(reverse("cats:rentals_list"))

    def show_rented_cats():
        rentals = Rental.objects.filter(user=user)
        return render(request, "cats/rentals_list.html", {"rentals": rentals})

    user = request.user
    if request.method == "POST":
        if user.is_authenticated:
            if request.POST.get("rent"):
                handle_rent()
                return congrats_mail(request, cat_id)
            else:
                handle_return()
    """
    if request.method == "GET":
    """
    return show_rented_cats()
