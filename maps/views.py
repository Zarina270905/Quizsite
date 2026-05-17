from django.shortcuts import render
from django.conf import settings
from quizzes.views import menu

def show_map(request):
    context = {
        'title': 'Карта',
        'menu': menu,
        'hide_categories': True,
        'maps_api_key': settings.MAPS_API_KEY,
    }
    return render(request, 'maps/map.html', context)