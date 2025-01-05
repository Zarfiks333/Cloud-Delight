from django.urls import path
from services.views import *

app_name = 'services'

urlpatterns = [
    path('', indexView, name='serviceshome'),
    path('service/<slug:slug>/', serviceDetail, name='service_detail'),
]
