import datetime

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column


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

    def clean(self):
        cleaned_data = super(RentalForm, self).clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")

        if date_from < datetime.date.today():
            raise forms.ValidationError("Cannot pick date from the past")
        if date_from > date_to:
            raise forms.ValidationError("'Date to' must be further than 'date from'")

        return cleaned_data


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

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")

        if date_from < datetime.date.today():
            raise forms.ValidationError("Cannot pick date from the past")
        if date_from > date_to:
            raise forms.ValidationError("'Date to' must be further than 'date from'")

        return cleaned_data
