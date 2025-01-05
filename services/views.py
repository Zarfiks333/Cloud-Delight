from django.shortcuts import render, get_object_or_404
from .models import Service

def indexView(request):
    services = Service.objects.all()
    context = {
        'title': 'CloudDelight | Услуги',
        'services': services,
    }
    return render(request, 'services.html', context=context)


def serviceDetail(request, slug):
    service = get_object_or_404(Service, slug=slug)

    context = {
        'title': f'CloudDelight | {service.name}',  # Название услуги в title
        'service': service,  # Передаем только эту услугу
    }
    return render(request, 'services/service_detail.html', context=context)
