import datetime
from django import forms
from django.forms import ModelForm

from .models import Classification, Forecast

class DateInput(forms.DateInput):
    input_type = 'date'

class ForecastForm(ModelForm):
    class Meta:
        model = Forecast
        fields = '__all__'
        widgets = {
            'date_st': DateInput(),
            'date_end': DateInput(),
        }

class ClassificationForm(ModelForm):
    class Meta:
        model = Classification
        fields = '__all__'
