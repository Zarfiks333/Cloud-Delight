from django.urls import path
from cart.views import *

app_name = 'cart'

urlpatterns = [
    path('', view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
]