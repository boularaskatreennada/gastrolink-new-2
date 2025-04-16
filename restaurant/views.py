from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant
from .forms import RestaurantForm

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'pdg/restaurants.html', {'restaurants': restaurants})

def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurants')
    else:
        form = RestaurantForm()
    return render(request, 'pdg/addRest.html', {'form': form})

def edit_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            return redirect('restaurants')
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'pdg/addRest.html', {'form': form})

def delete_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurants')
    return render(request, 'pdg/restDeleteconfirm.html', {'restaurant': restaurant})

