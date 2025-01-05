from django.urls import path
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', indexView, name='mainhome'),
    path('user-agreement/', polzView, name='polzview'),
    path('privacy-policy/', poltView, name='poltview'),
    path('search/', search, name='search'),
]
