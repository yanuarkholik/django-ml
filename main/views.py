import pandas as pd
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

# Create your views here.
from .models import Data, Customer, Forecast
from .forms import ForecastForm, ClassificationForm
from .forecast import predict

def index(request):
    return render(request, 'base.html')

def error(request):
    return render(request, '404.html')

def forecast(request):
    form = ForecastForm()
    result = []
    eval = []
    if request.method == 'POST':
        form = ForecastForm(request.POST)

        model = request.POST['model']
        cd = request.POST['comp_code']
        start = request.POST['date_st']
        end = request.POST['date_end']

        if form.is_valid():
            item = form.save(commit=False)
            result, eval = predict(model, cd, start, end)
            item.save()
            return HttpResponseRedirect('/forecast/')
    else: 
        form = ForecastForm()

    print(result)
    return render(request, 'pages/forecast.html', {'form':form, 'value': result, 'eval': eval})

def classification(request):
    form = ClassificationForm()
    if request.method == 'POST':
        form = ClassificationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/classification/')
    else: 
        form = ClassificationForm()

    return render(request, 'pages/classification.html', {'form':form})

class home(ListView):
    model = Customer
    template_name = 'pages/home.html'
    context_object_name = 'customer'
