from django.shortcuts import render, redirect
from product.models import *
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart = request.session.get('cart', [])
    

    cart.append(product_id)
    request.session['cart'] = cart
    

    return JsonResponse({
        'message': f'Товар {product.name} добавлен в корзину',
        'cart_count': len(cart),
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    
    if product_id in cart:
        cart.remove(product_id)
        request.session['cart'] = cart

    return JsonResponse({
        'message': f'Товар {product_id} удален из корзины',
        'cart_count': len(cart),
    })


def view_cart(request):
    cart = request.session.get('cart', [])
    
    products_in_cart = []
    
    for product_id in cart:
        product = get_object_or_404(Product, id=product_id)
        products_in_cart.append(product)

    context = {
        'title': 'CloudDelight | Корзина',
        'products_in_cart': products_in_cart,
        }
    
    return render(request, 'cart.html', context=context)

