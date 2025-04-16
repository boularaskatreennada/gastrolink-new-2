# views.py
from django.shortcuts import render
from .models import *

def menu_management(request):
    categories = MainMenu.objects.all()
    selected_category_id = request.GET.get('category')

    if selected_category_id:
        dishes = Dish.objects.filter(menu_id=selected_category_id)
    else:
        dishes = Dish.objects.all()

    context = {
        'categories': categories,
        'dishes': dishes,
        'selected_category_id': int(selected_category_id) if selected_category_id else None,
    }

    return render(request, 'pdg/menu.html', context)
