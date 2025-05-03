from gettext import translation
from itertools import count
import json
from django.http import Http404
from django.shortcuts import render
from django.utils.dateparse import parse_date

from reservations.models import Table
from restaurant.decorators import *
from .models import Order, OrderDish
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import date
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from menu.models import DailyMenu, DailyMenuDish
from .models import Delivery, Order, Dish,OrderDish, OrderMode, OrderStatus 
from restaurant.models import Chef, Server
from django.db import transaction
from django.db.models import F, Q ,Count ,Sum
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
@waiter_required
def orders_list(request):
    #  Find the restaurant 
    server     = get_object_or_404(Server, user=request.user)
    restaurant = server.restaurant
    status = request.GET.get('filterStatus')
    order_type = request.GET.get('filterType')
    table_number = request.GET.get('filterTable')
    payment_status = request.GET.get('filterPayment')
    search = request.GET.get('search')
    date_str = request.GET.get('date')

    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = None
            
    else:
        selected_date = timezone.localdate()

    # orders by that date
    orders = (
        Order.objects
             .filter(
                 restaurant=restaurant,
                 order_date__date=selected_date  
             ).annotate(
                items_count=Count('orderdish', distinct=True),
                total_price=Sum(F('orderdish__quantity') * F('orderdish__dish__price')
                )).order_by('-order_date')
             .prefetch_related('orderdish_set__dish')
             
    )

    if status:
        orders = orders.filter(status=status)
    if order_type:
        orders = orders.filter(mode=order_type)
    if table_number:
        orders = orders.filter(table__id=table_number)
    if payment_status:
        orders = orders.filter(payment_status=payment_status)
    if search:
        orders = orders.filter(
            Q(table__name__icontains=search) |
            Q(server__user__username__icontains=search) |
            Q(orderdish__dish__name__icontains=search)
        ).distinct()
    
    return render(request, 'serveur/ordersList.html', {
        'orders': orders,
        'selected_date': selected_date,
    })



@chef_required
def order_list_chef(request):
       # get chefs restaurant
    chef = get_object_or_404(Chef, user=request.user)
    restaurant = chef.restaurant
    filter_type = request.GET.get('filter_type')
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = None
            
    else:
        selected_date = timezone.localdate()

    orders = (
        Order.objects
             .filter(
                 restaurant=restaurant,
                 order_date__date=selected_date  
             ).exclude(status='cancelled')
             .order_by('-order_date')
             .prefetch_related('orderdish_set__dish')
    )
    if filter_type:
        orders = orders.filter(mode=filter_type)

    return render(request, 'chef/ordersListChef.html', {
        'orders': orders,
        'restaurant': restaurant
    })

@waiter_required
def edit_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    tables = Table.objects.filter(restaurant=order.restaurant)
    # Get all dishes in today's menu 
    today_menu = DailyMenu.objects.filter(
        restaurant=order.restaurant,
        date=timezone.localdate()
    ).first()

    if not today_menu:
        raise Http404("No menu for today")

    menu_entries = DailyMenuDish.objects.filter(menu=today_menu).select_related('dish')

    # Prepare existing order items for JS cart initialization
    order_items = []
    for od in order.orderdish_set.select_related('dish').all():
        order_items.append({
            'id': od.dish.id,
            'name': od.dish.name,
            'price': float(od.dish.price),
            'quantity': od.quantity,
        })

    context = {
        'menu_entries': menu_entries,
        'order_items_json': json.dumps(order_items),  # pass as JSON string
        'order': order,
        'tables': tables,  # pass tables here
    }

    return render(request, 'serveur/takeOrder.html', context)

@chef_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(OrderStatus.choices):
            order.status = new_status
            order.save()
    return redirect('ordersList')

@waiter_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if request.method == 'POST':
        order.status = OrderStatus.CANCELLED
        order.save()
    return redirect('ordersList')

@delivery_required
def delivery_orders(request):
    order= Delivery.objects.all()
    Delivery.objects.filter(delivery_person=request.user)
    return render(request, 'livreur/DeliveryOrders.html', {
        'orders': order, })

@delivery_required
def update_delivery_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(DeliveryStatus.choices):
            order.status = new_status
            order.save()
    return redirect('DeliveryOrders')

@waiter_required
def take_order(request):
    # 1️⃣ Find the restaurant from the logged-in waiter
    server     = get_object_or_404(Server, user=request.user)
    restaurant = server.restaurant
    tables = Table.objects.filter(restaurant=restaurant)

    # 2️⃣ Grab (or bail if missing) today’s DailyMenu
    today = date.today()
    try:
        today_menu = DailyMenu.objects.get(restaurant=restaurant, date=today)
        # 3️⃣ Fetch all the dishes on that menu
        menu_entries = DailyMenuDish.objects.filter(menu=today_menu).select_related('dish')
    except DailyMenu.DoesNotExist:
        menu_entries = []

    # 4️⃣ Render, passing the list of entries
    return render(request, 'serveur/takeOrder.html', {
        'menu_entries': menu_entries,
        'tables':       tables,
        })

@waiter_required
def place_order(request):
    server = get_object_or_404(Server, user=request.user)
    restaurant = server.restaurant
    table_id = request.POST.get('table_id')
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)
    today = date.today() # Use timezone-aware date
    order_id = request.POST.get('order_id')  # <-- NEW
    # Use transaction to lock rows and avoid race conditions
    with transaction.atomic():
        today_menu = DailyMenu.objects.filter(
            restaurant=restaurant,
            date=today
        ).first()
        if not today_menu:
          #  messages.error(request, "No menu for today.")
            return redirect('takeOrder')

        if request.method == 'POST':
            item_ids = request.POST.getlist('item_id')
            quantities = request.POST.getlist('quantity')
            note = request.POST.get('note', '')

            # Lock the menu entries for update
            menu_entries = DailyMenuDish.objects.select_for_update().filter(menu=today_menu)
            menu_map = {entry.dish_id: entry for entry in menu_entries}
            # --- NEW LOGIC ---
            if order_id:
                order = get_object_or_404(Order, pk=order_id)
                order.table = table
                
                # Restore original stock quantities
                if order.orderdish_set.exists():  # Prevent None error
                    original_menu = order.orderdish_set.first().dish.dailymenudish_set.first().menu
                    for old_item in order.orderdish_set.all():
                        DailyMenuDish.objects.filter(
                            menu=original_menu,
                            dish=old_item.dish
                        ).update(
                            current_quantity=F('current_quantity') + old_item.quantity
                        )
                
                order.orderdish_set.all().delete()
                order.save()
            else:
                order = Order.objects.create(
                    server     = server,
                    restaurant = restaurant,
                    table      = table,
                    status     = OrderStatus.PENDING,
                    mode       = OrderMode.SERVED,
                )

            for dish_id_str, qty_str in zip(item_ids, quantities):
                try:
                    dish_id = int(dish_id_str)
                    qty = int(qty_str)
                except ValueError:
                    continue  # skip invalid data

                if qty <= 0:
                    continue

                entry = menu_map.get(dish_id)
                if not entry:
                  #  messages.error(request, f"Dish ID {dish_id} not on today's menu.")
                    continue

                # Check quantity and decrement safely
                if qty > entry.current_quantity:
                    qty = entry.current_quantity

                if qty <= 0:
                    continue

                # Create order item
                OrderDish.objects.create(
                    order=order,
                    dish=entry.dish,
                    quantity=qty
                )

                # Decrement available quantity using F expression (safe for concurrency)
                DailyMenuDish.objects.filter(pk=entry.pk).update(
                    current_quantity=F('current_quantity') - qty
                )

            #messages.success(request, f"Order #{order.pk} created!")
            return redirect('takeOrder')

    
    

