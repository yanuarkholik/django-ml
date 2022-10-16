from django.urls import path 

from django.conf import settings
from django.conf.urls.static import static

from main import views


urlpatterns = [
    path('', views.index, name='index'),
    path('error/', views.error, name='error-page'),
    path('home/', views.home.as_view(), name='home-page'),
    
    path('forecast/', views.forecast, name='forecast-page'),
    path('classification/', views.classification, name='classification-page'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)