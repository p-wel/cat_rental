"""
Creating forms to use in app
"""

import datetime

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column

from cats.models import Rental


class RentalForm(forms.ModelForm):
    """Form used to create a new Rental object"""

    class Meta:
        model = Rental
        fields = ['cat', 'user', 'rental_date', 'return_date']
        widgets = {
            'cat': forms.HiddenInput,
            'user': forms.HiddenInput,
            'rental_date': forms.DateInput(
                attrs={
                    'class': 'datepicker',
                    'type': 'date',
                    'placeholder': 'DD-MM-YYYY'
                }
            ),
            'return_date': forms.DateInput(
                attrs={
                    'class': 'datepicker',
                    'type': 'date',
                    'placeholder': 'DD-MM-YYYY'
                }
            ),
        }


class SearchForm(forms.Form):
    """Search form used in Cats lists"""
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
                'type': 'date',
                'placeholder': 'DD-MM-YYYY'
            }
        )
    )

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
        """Cleans the form"""
        cleaned_data = super(SearchForm, self).clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')

        """Raise error if "date_from" is from the past"""
        if date_from < datetime.date.today():
            raise forms.ValidationError('Cannot pick date from the past')

        """Raise error if dates are picked backwards"""
        if date_from > date_to:
            raise forms.ValidationError('"Date to" must be further than "date from"')

        return cleaned_data
