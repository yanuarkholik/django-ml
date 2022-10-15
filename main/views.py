import pandas as pd
from django.shortcuts import render
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

# Create your views here.
from .models import Data, Customer
from .forms import CustomerForm, DataForm
# from .clean import read_csv

def index(request):
    return render(request, 'base.html')

def error(request):
    return render(request, '404.html')

class home(ListView):
    model = Customer
    template_name = 'pages/home.html'
    context_object_name = 'customer'

class CreateCustomer(View):
    def get(self, request):
        fname = request.GET.get('fname')
        lname = request.GET.get('lname')

        obj = Customer.objects.create(
            first_name = fname,
            last_name = lname
        )
        customer = {'id': obj.id, 'first_name': obj.first_name, 'last_name': obj.last_name }
        context = {
            'customer': customer
        }
        return JsonResponse(context)
