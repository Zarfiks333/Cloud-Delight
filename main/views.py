from django.shortcuts import render, redirect
from product.models import Product
from django.template.loader import render_to_string
from django.http import JsonResponse
from services.models import Service

def indexView(request):
    context = {'title': 'CloudDelight'}
    return render(request, 'index.html', context=context)

def polzView(request):
    context = {'title': 'CloudDelight | Политика соглашение'}
    return render(request, 'wiki/polz.html', context=context)

def poltView(request):
    context = {'title': 'CloudDelight | Политика конфиденциальности '}
    return render(request, 'wiki/polit.html', context=context)


def search(request):
    query = request.GET.get('q', '')
    
    # Если запрос не является AJAX, перенаправляем на главную страницу
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if query:
            # Перенаправляем на главную страницу с поисковым запросом в URL
            return redirect('main:mainhome')  # main:mainhome - название вашего url для главной страницы
    
    # Если запрос является AJAX-запросом
    if query:
        # Ищем в моделях продуктов и услуг
        products = Product.objects.filter(name__icontains=query)
        services = Service.objects.filter(name__icontains=query)
        
        # Возвращаем только результаты в JSON формате
        results_html = render_to_string('search_results.html', {
            'products': products,
            'services': services,
        })
        return JsonResponse({'results_html': results_html})
    
    return JsonResponse({'results_html': ''})