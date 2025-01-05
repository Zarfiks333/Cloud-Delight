import json
from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.utils.timezone import now

def productView(request):
    categories = Category.objects.all()
    context = {
        'title': 'CloudDelight | Товары',
        'categories': categories
        }
    return render(request, 'product.html', context=context)

def category_detail(request, category_slug):

    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    best_sellers = Product.objects.filter(is_best_seller=True, category=category)
    products_with_discounts = Product.objects.filter(discount__gt=0, category=category)

    context = {
            'title': f'CloudDelight | {category.name}',
            'category': category,
            'products': products,
            'best_sellers': best_sellers,
            'products_with_discounts': products_with_discounts,
            }
    return render(request, 'product/category_detail.html', context=context)


from django.utils.timezone import now

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category)

    original_price = product.get_discounted_price() if product.discount > 0 else product.price
    discounted_price = original_price
    promo_code_valid = False  

    promo_code = request.GET.get("promo_code")
    if promo_code:
        promo = PromoCode.objects.filter(code=promo_code).first()
        if promo and promo.is_valid():
            discounted_price = original_price * (1 - promo.discount / 100)
            promo_code_valid = True  

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "original_price": float(original_price),
            "discounted_price": float(discounted_price) if promo_code_valid else None, 
            "promo_code_valid": promo_code_valid,  
        })

    context = {
        'title': f'CloudDelight | {product.name}',
        'product': product,
        'original_price': original_price,
        'discounted_price': discounted_price,
    }
    return render(request, 'product/product_detail.html', context)



def buy_product(request, category_slug, product_slug):
    if request.method == "POST":
        # Парсим тело запроса JSON
        try:
            data = json.loads(request.body)
            promo_code = data.get("promo_code")
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Неверный формат данных."}, status=400)

        category = get_object_or_404(Category, slug=category_slug)
        product = get_object_or_404(Product, slug=product_slug, category=category)

        # Если промокод есть, проверяем его
        if promo_code:
            promo = PromoCode.objects.filter(code=promo_code).first()
            if promo:
                # Если промокод истёк, просто игнорируем его
                if promo.times_used >= promo.usage_limit:
                    promo_code = None
                else:
                    # Если промокод действителен, увеличиваем количество использований
                    if promo.is_valid():
                        promo.times_used += 1
                        promo.save()

        # Возвращаем успешный ответ, независимо от состояния промокода
        return JsonResponse({
            "success": True,
            "message": "Покупка завершена успешно." + (" (Промокод не учтён, т.к. он исчерпан)." if promo_code is None else "")
        })

    return JsonResponse({"success": False, "message": "Неверный запрос."}, status=400)

