from django.urls import path
from product.views import *

app_name = 'product'

urlpatterns = [
    path('', productView, name='producthome'),
    path('category/<slug:category_slug>/', category_detail, name='category_detail'),  # Страница категории
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),  # Страница продукта
    path('buy/<slug:category_slug>/<slug:product_slug>/', buy_product, name='buy_product'),
]
