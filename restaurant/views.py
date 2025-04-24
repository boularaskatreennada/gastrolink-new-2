from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from .decorators import pdg_required, manager_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def pdg_dashboard(request):
    return render(request, 'pdg/dashboard.html') 


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['display_username'] = user.get_full_name() or user.username
            if user.user_type == 'PDG':
                return redirect('pdg_dashboard')
            elif user.user_type == 'MANAGER':
                return redirect('manager_dashboard')
            ''' elif user.user_type == 'CHEF':
                return redirect('chef_dashboard')
            elif user.user_type == 'SERVER':
                return redirect('server_dashboard')
            elif user.user_type == 'DELIVERY':
                return redirect('delivery_dashboard')
            elif user.user_type == 'CLIENT':
                return redirect('client_dashboard')
            elif user.user_type == 'SUPPLIER':
                return redirect('supplier_dashboard')'''
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

@pdg_required
def pdg_dashboard(request):
    if request.user.user_type != 'PDG':
        return redirect('login')
    return render(request, 'pdg/dashboard.html')

@manager_required
def manager_dashboard(request):
    if request.user.user_type != 'MANAGER':
        return redirect('login')
   
    restaurant = request.user.manager.restaurant
    return render(request, 'manager/dashboard.html', {'restaurant': restaurant})

@pdg_required
def restaurant_list(request): 
    selected_city = request.GET.get('city')
    restaurants = Restaurant.objects.select_related('manager__user').all()
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

@pdg_required
def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('restaurants')
    else:
        form = RestaurantForm()
    return render(request, 'pdg/addRest.html', {'form': form})

@pdg_required
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

@pdg_required
def delete_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurants')
    return render(request, 'pdg/restaurants.html', {'restaurant': restaurant})

@pdg_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    
    return render(request, 'pdg/addEmployee.html', {'form': form})

@pdg_required
def employee_list(request):
    highlight_manager = request.GET.get('highlight')
    
    managers = Manager.objects.select_related('user', 'restaurant').all()
    suppliers = Supplier.objects.select_related('user').all()
    
    return render(request, 'pdg/employees.html', {
        'managers': managers,
        'suppliers': suppliers,
        'highlight_manager': highlight_manager
    })

User = get_user_model()

@pdg_required
def edit_employee(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    try:
        if user.user_type == 'MANAGER':
            employee = Manager.objects.get(user=user)
        elif user.user_type == 'SUPPLIER':
            employee = Supplier.objects.get(user=user)
        else:
            return redirect('employee_list')
    except (Manager.DoesNotExist, Supplier.DoesNotExist):
        return redirect('employee_list')

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            if user.user_type == 'MANAGER':
                # Get the new restaurant from the form
                new_restaurant = form.cleaned_data['restaurant']
                
                # Check if the restaurant already has a different manager
                if Manager.objects.filter(restaurant=new_restaurant).exclude(user=user).exists():
                    form.add_error('restaurant', 'This restaurant already has a manager.')
                    context = {
                        'form': form,
                        'is_edit': True,
                        'user_type': user.user_type,
                    }
                    return render(request, 'pdg/add_employee.html', context)
                
                employee.restaurant = new_restaurant
                employee.status = form.cleaned_data['status']
                employee.save()
                
            elif user.user_type == 'SUPPLIER':
                employee.address = form.cleaned_data['address']
                employee.save()
            
            return redirect('employee_list')
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'user_type': user.user_type,
        }
        
        if user.user_type == 'MANAGER':
            initial_data.update({
                'restaurant': employee.restaurant,
                'status': employee.status,
            })
        elif user.user_type == 'SUPPLIER':
            initial_data.update({
                'address': employee.address,
            })
        
        form = EmployeeForm(instance=user, initial=initial_data)

    context = {
        'form': form,
        'is_edit': True,
        'user_type': user.user_type,
    }
    return render(request, 'pdg/addEmployee.html', context)

@pdg_required
def delete_manager(request, pk):
    manager = get_object_or_404(Manager, pk=pk)
    if request.method == 'POST':
        manager.user.delete()
        return redirect('employee_list')
    return redirect('employee_list')

@pdg_required
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.user.delete()
        return redirect('employee_list')
    return redirect('employee_list')














@manager_required
def employee_manager_list(request):
    waiters = Server.objects.all()
    chefs = Chef.objects.all()
    DeliveryPersons = DeliveryPerson.objects.all()
    return render(request, 'manager/employee.html', {
        'waiters': waiters,
        'chefs': chefs,
        'DeliveryPersons': DeliveryPersons
    })

@manager_required
def add_staff_employee(request):
    form = StaffEmployeeForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        role = data['role']
        model = {'chef': Chef, 'server': Server, 'delivery': DeliveryPerson}.get(role)

        if model:
            model.objects.create(
                name=data['name'],
                email=data['email'],
                phone=data['phone'],
                password=data['password'],
                restaurant=data['restaurant'],
                status=data['status']
            )
            return redirect('employee_manager_list')

    return render(request, 'manager/addEmployee.html', {'form': form})

@manager_required
def edit_staff_employee(request, role, pk):
    model = {'chef': Chef, 'server': Server, 'delivery': DeliveryPerson}.get(role)
    instance = get_object_or_404(model, pk=pk)

    initial_data = {
        'name': instance.name,
        'email': instance.email,
        'phone': instance.phone,
        'password': instance.password,
        'restaurant': instance.restaurant,
        'status': instance.status,
        'role': role,
    }

    form = StaffEmployeeForm(request.POST or None, initial=initial_data)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        instance.name = data['name']
        instance.email = data['email']
        instance.phone = data['phone']
        instance.password = data['password']
        instance.restaurant = data['restaurant']
        instance.status = data['status']
        instance.save()
        return redirect('employee_manager_list')

    return render(request, 'manager/addEmployee.html', {'form': form, 'employee': instance})

@manager_required
def delete_staff_employee(request, role, pk):
    model = {'chef': Chef, 'server': Server, 'delivery': DeliveryPerson}.get(role)
    employee = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        employee.delete()
        return redirect('employee_manager_list')

    return render(request, 'manager/employee.html', {'employee': employee})
