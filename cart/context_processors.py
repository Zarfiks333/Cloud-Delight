from django.http import HttpRequest

def cart_count(request: HttpRequest):
    cart = request.session.get('cart', [])
    cart_count = len(cart)
    return {'cart_count': cart_count}
