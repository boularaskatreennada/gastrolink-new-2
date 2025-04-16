from django.urls import path
from . import views

urlpatterns = [
    # Restaurant CRUD
    path('restaurants/', views.restaurant_list, name='restaurants'),
    path('restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurants/edit/<int:pk>/', views.edit_restaurant, name='edit_restaurant'),
    path('restaurants/delete/<int:pk>/', views.delete_restaurant, name='delete_restaurant'),
    path('add-employee/', views.add_employee, name='add_employee'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/edit/<str:role>/<int:id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<str:role>/<int:id>/', views.delete_employee, name='delete_employee'),
    path('add-employee/', views.add_employee, name='add_employee'),
]  