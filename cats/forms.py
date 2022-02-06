from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column


class CalendarForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(
        format='%d-%m-%Y',
        attrs={'class': 'datepicker', 'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(
        format='%d-%m-%Y',
        attrs={'class': 'datepicker', 'type': 'date'}))


class RentalForm(CalendarForm):
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


class ListForm(CalendarForm):
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
