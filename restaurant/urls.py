from django.urls import path
from . import views

urlpatterns = [
    path('restaurants/', views.restaurant_list, name='restaurants'),
    path('restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurants/edit/<int:pk>/', views.edit_restaurant, name='edit_restaurant'),
    path('restaurants/delete/<int:pk>/', views.delete_restaurant, name='delete_restaurant'),
]  