import datetime

from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from cats.models import Rental


class RentalForm(forms.Form):
    date_from = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'datepicker',
                'type': 'date',
                'placeholder': 'DD-MM-YYYY'
            }
        ),
        initial=datetime.date.today())
    date_to = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'datepicker',
                   'type': 'date'
                   }
        ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date_from')
            ),
            Row(
                Column('date_to')
            ),
            Submit('rent', 'Rent')
        )

    # def clean_rental_date(self):
    #     rental_date = self.cleaned_data.get("rental_date")
    #     if rental_date < datetime.date.today():
    #         raise forms.ValidationError("Cannot pick date from the past")
    #     else:
    #         return rental_date
    #
    # def clean_return_date(self):
    #     rental_date = self.cleaned_data.get("rental_date")
    #     return_date = self.cleaned_data.get("return_date")
    #     if rental_date > return_date:
    #         raise forms.ValidationError("Date from must be further than date to")
    #     else:
    #         return return_date


# Change RentalForm(forms.Form) into ModelForm. Add 'rental_date' and 'return_date' validation
# class RentalForm(ModelForm):
#     class Meta:
#         model = Rental
#         fields = ['rental_date', 'return_date']
#         widgets = {
#             'rental_date': forms.DateInput(
#                 attrs={
#                     'class': 'datepicker',
#                     'type': 'date',
#                     'placeholder': 'DD-MM-YYYY'
#                 }),
#             'return_date': forms.DateInput(
#                 attrs={
#                     'class': 'datepicker',
#                     'type': 'date',
#                     'placeholder': 'DD-MM-YYYY'
#                 }),
#         }


class SearchForm(forms.Form):
    date_from = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'datepicker',
                'type': 'date',
                'placeholder': 'DD-MM-YYYY'
            }
        ),
        initial=datetime.date.today())
    date_to = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'class': 'datepicker',
                'type': 'date'
            }
        ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date_from')
            ),
            Row(
                Column('date_to')
            ),
            Submit('search', 'Search')
        )

    def clean_date_from(self):
        date_from = self.cleaned_data.get("date_from")
        if date_from < datetime.date.today():
            raise forms.ValidationError("Cannot pick date from the past")
        else:
            return date_from

    def clean_date_to(self):
        date_from = self.cleaned_data.get("date_from")
        date_to = self.cleaned_data.get("date_to")
        if date_from > date_to:
            raise forms.ValidationError("'Date to' must be further than 'date from'")
        else:
            return date_to
