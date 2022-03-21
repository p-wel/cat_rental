"""
Creating forms to use in app
"""

import datetime

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column


class RentalForm(forms.Form):
    """Rental form with calendar widget"""
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


class SearchForm(forms.Form):
    """Search form with calendar widget"""
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
