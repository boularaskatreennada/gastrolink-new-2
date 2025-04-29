from django.shortcuts import render
from django.utils.dateparse import parse_date

from restaurant.decorators import *
from .models import Order, OrderDish
from datetime import datetime
from django.contrib.auth.decorators import login_required

@manager_required
def orders_list(request):
    """Afficher la liste des commandes filtrées par date"""
    restaurant = request.user.manager.restaurant 

    date_str = request.GET.get('date')
    orders = []

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            orders = Order.objects.filter(
                restaurant=restaurant,
                order_date__date=selected_date
            ).order_by('-order_date')
        except ValueError:
            selected_date = None
            orders = []
    else:
        selected_date = None

    return render(request, 'manager/client_orders.html', {
        'orders': orders,
        'selected_date': selected_date
    })
