from crispy_forms import helper
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from cats.forms import RentalForm, SearchForm
from cats.models import Cat, Species, Breed, Rental


class IndexView(TemplateView):
    template_name = 'cats/index.html'


class AboutView(TemplateView):
    template_name = 'cats/about.html'


class SpeciesListView(ListView):
    model = Species
    template_name = 'cats/species.html'


# CBV Explore
class ExploreListView(ListView):
    model = Cat
    template_name = 'cats/explore_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


def explore_list(request):
    cats = Cat.objects.all()
    search_form = SearchForm()
    if request.method == "GET":
        search_form.helper.form_action = reverse("cats:explore_list")
        context = {'all_cats': cats, 'search_form': search_form}
        return render(request, 'cats/explore_list.html', context)
    else:
        breeds = Breed.objects.all()
        date_from = request.POST.get("date_from")
        date_to = request.POST.get("date_to")
        cats_available = Cat.objects.filter_by_dates(date_from, date_to)
        context = {'breeds_list': breeds, 'cats_list': cats_available,
                   'search_form': search_form}
        search_form.helper.form_action = reverse("cats:explore_list")
        return render(request, 'cats/explore_list.html', context)


class CatsListView(ListView):
    model = Cat
    template_name = 'cats/cats_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


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
#     cat = Cat.objects.get(pk=cat_id)
#     context = {"cat": cat}
#     return render(request, 'cats/details.html', context)

class RentalCreateView(CreateView):
    model = Rental
    fields = ['cat', 'user', 'rental_date', 'return_date']
    template_name = 'cats/rental_dates.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rental_form'] = RentalForm()
        return context

    def get_initial(self):
        return {'user': self.request.user, 'cat': self.kwargs['cat_id']}


# OLD FUNCTION VIEW
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


def congrats_mail(request, cat_id):
    cat = Cat.objects.get(pk=cat_id)
    congrats_template = render_to_string('cats/congrats_mail_template.html', {'cat': cat})

    send_mail('Congrats, cat rented!',
              congrats_template,
              '',
              [request.user.email],
              fail_silently=False)
    return render(request, 'cats/congrats.html', {'cat': cat})
