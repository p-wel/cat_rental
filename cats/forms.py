from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class CatRentalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('rent', 'Rent'))


class DateInput(forms.DateInput):
    input_type = 'date'


class CalendarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(DateInput())
