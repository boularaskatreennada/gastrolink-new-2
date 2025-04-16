from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant
from .forms import *

def restaurant_list(request): 
    selected_city = request.GET.get('city')
    if selected_city:
        restaurants = Restaurant.objects.filter(city=selected_city)
    else:
        restaurants = Restaurant.objects.all()

    cities = Restaurant.objects.values_list('city', flat=True).distinct()
    return render(request, 'pdg/restaurants.html', {
        'restaurants': restaurants,
        'cities': cities,
        'selected_city': selected_city
    })

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

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            role = form.cleaned_data['role']
            print("👉 Role received:", role) 
            if role == 'manager':
                Manager.objects.create(
                    name=form.cleaned_data['full_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    password=form.cleaned_data['password'],
                    status=form.cleaned_data['status'],
                    restaurant=form.cleaned_data['restaurant'],
                )
            elif role == 'supplier':
                Supplier.objects.create(
                    name=form.cleaned_data['full_name'],
                    phone=form.cleaned_data['phone'],
                    email=form.cleaned_data['email'],
                    address=form.cleaned_data['address'],
                )
                print("✅ Supplier successfully created and redirected.")
            return redirect('employee_list')
            

    else:
        form = EmployeeForm()
    return render(request, 'pdg/addEmployee.html', {'form': form})

#  Liste des managers et fournisseurs
def employee_list(request):
    managers = Manager.objects.all()
    suppliers = Supplier.objects.all()
    return render(request, 'pdg/employees.html', {
        'managers': managers,
        'suppliers': suppliers
    })

#  Modifier un employé (manager ou supplier)
def edit_employee(request, role, id):
    instance = None
    if role == 'manager':
        instance = get_object_or_404(Manager, id=id)
    elif role == 'supplier':
        instance = get_object_or_404(Supplier, id=id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            if role == 'manager':
                instance.name = form.cleaned_data['full_name']
                instance.email = form.cleaned_data['email']
                instance.phone = form.cleaned_data['phone']
                instance.password = form.cleaned_data['password']
                instance.restaurant = form.cleaned_data['restaurant']
            elif role == 'supplier':
                instance.name = form.cleaned_data['full_name']
                instance.email = form.cleaned_data['email']
                instance.phone = form.cleaned_data['phone']
                instance.address = form.cleaned_data['address']
            instance.save()
            return redirect('employee_list')
    else:
        # Initialisation du formulaire avec les données existantes
        initial = {
            'full_name': instance.name,
            'email': instance.email,
            'phone': instance.phone,
            'role': role
        }
        if role == 'manager':
            initial['password'] = instance.password
            initial['restaurant'] = instance.restaurant
        elif role == 'supplier':
            initial['address'] = instance.address
        form = EmployeeForm(initial=initial)
    
    return render(request, 'pdg/addEmployee.html', {'form': form, 'role': role, 'id': id})

#  Supprimer un employé
def delete_employee(request, role, id):
    if role == 'manager':
        obj = get_object_or_404(Manager, id=id)
    elif role == 'supplier':
        obj = get_object_or_404(Supplier, id=id)
    else:
        return redirect('employee_list')
    
    obj.delete()
    return redirect('employee_list')