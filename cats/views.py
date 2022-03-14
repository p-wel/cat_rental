import datetime

from django.core.mail import send_mail
from django.http import HttpResponseRedirect, Http404
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


# CBV
# class ExploreListView(ListView):
#     model = Cat
#     template_name = 'cats/explore_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['search_form'] = SearchForm()
#         return context


def explore_list(request):
    cats = None
    search_form = SearchForm(request.GET or None)
    if search_form.is_valid():
        date_from = search_form.cleaned_data['date_from']
        date_to = search_form.cleaned_data['date_to']
        cats = Cat.objects.filter_by_dates(date_from, date_to)
    context = {'cats_list': cats, 'search_form': search_form}
    return render(request, 'cats/explore_list.html', context)


# CBV
# class CatsListView(ListView):
#     model = Cat
#     template_name = 'cats/cats_list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['search_form'] = SearchForm()
#         return context


# OLD FUNCTION VIEW
def cats_list(request, species_id):
    search_form = SearchForm()
    if request.method == "GET":
        search_form.helper.form_action = reverse("cats:list", args=[species_id])
        context = {'species_id': species_id, 'search_form': search_form}
        return render(request, 'cats/cats_list.html', context)
    else:
        breeds = Breed.objects.all()
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        cats_available = Cat.objects.filter_by_dates(date_from, date_to)
        context = {'breeds_list': breeds, 'cats_list': cats_available, 'species_id': species_id,
                   'search_form': search_form}
        search_form.helper.form_action = reverse("cats:list", args=[species_id])
        return render(request, 'cats/cats_list.html', context)


class CatDetailView(DetailView):
    model = Cat
    template_name = 'cats/details.html'


# OLD FUNCTION VIEW
# def cat_details(request, cat_id):
# cat = Cat.objects.get(pk=cat_id)
# context = {"cat": cat}
# return render(request, 'cats/details.html', context)


# CBV
# class RentalCreateView(CreateView):
#     model = Rental
#     fields = ['cat', 'user', 'rental_date', 'return_date']
#     template_name = 'cats/rental_dates.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rental_form'] = RentalForm()
#         return context
#
#     def get_initial(self):
#         return {'user': self.request.user, 'cat': self.kwargs['cat_id']}


# OLD FUNCTION VIEW TODO rental_dates.html - change crispy into regular Django form
# def cat_rental_dates(request, cat_id):
#     cat = get_object_or_404(Cat, pk=cat_id)
#     # date_from = request.POST.get("date_from")
#     # date_to = request.POST.get("date_to")
#     rental_form = RentalForm()
#     rental_form.helper.form_action = reverse("cats:rent_the_cat", args=[cat_id])
#     context = {"cat": cat, "rental_form": rental_form}
#     return render(request, 'cats/rental_dates.html', context)

# TODO try-except
def cat_rental_dates(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)
    rental_form = RentalForm()
    rental_form.helper.form_action = reverse("cats:rent_the_cat", args=[cat_id])
    context = {"cat": cat, "rental_form": rental_form}
    return render(request, 'cats/rental_dates.html', context)


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
        # keys = [
        #     key for key in request.POST.keys()
        #     if key.startswith("cat_")
        # ]
        # key = int(keys[0].split("_")[1])
        # """
        # keys - taking out proper cat's id from submit button in:
        #         /rentals_history.html
        #             button name="cat_{{ rental.cat.id }}"
        # """
        # cat = Cat.objects.get(pk=key)
        #
        # # TODO: last() should be changed for this rental's id
        # # TODO: also, it should make Rental.valid = False
        #
        # rental = Rental.objects.filter(user=user, cat=cat).last()
        # """
        # rental - last rental of given cat, rented by given user
        # last() method to avoid assigning older rentals that weren't signed as returned before
        # """
        # rental.return_date = timezone.now()
        # rental.valid = False
        # rental.save()

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
        if request.POST.get("rent"):
            return handle_rent()
        else:
            return handle_return()
            # return handle_return(rental_id=rental.id)

    rentals = Rental.objects.filter(user=user)
    return render(request, "cats/rentals_history.html", {'rentals': rentals})


def rentals_history(request):
    user_rentals = Rental.objects.filter(user=request.user)
    today = datetime.date.today()
    return render(request, "cats/rentals_history.html", {'user_rentals': user_rentals, 'today': today})


def congrats_mail(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    congrats_template = render_to_string('cats/congrats_mail_template.html', {'cat': cat})

    send_mail('Congrats, cat rented!',
              congrats_template,
              '',
              [request.user.email],
              fail_silently=False)
    return render(request, 'cats/congrats.html', {'cat': cat})
