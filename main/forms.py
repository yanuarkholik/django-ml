from dataclasses import field
from django.forms import ModelForm

from .models import Customer, Data

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class DataForm(ModelForm):
    class Meta:
        model = Data
        fields = ('file',)
