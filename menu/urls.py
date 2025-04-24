from django.urls import path
from . import views

urlpatterns = [
    # Menu and Plates
    path('menu/', views.menu_view, name='menu'),
    path('menu/add/', views.add_plate, name='add_plate'),
    path('menu/edit/<int:pk>/', views.edit_plate, name='edit_plate'),
    path('menu/delete/<int:pk>/', views.delete_plate, name='delete_plate'),

    # Ingredients
    path('ingredients/', views.ingredients_view, name='ingredients'),
    path('ingredients/add/', views.add_ingredient, name='add_ingredient'),
    path('ingredients/edit/<int:pk>/', views.edit_ingredient, name='edit_ingredient'),
    path('ingredients/delete/<int:pk>/', views.delete_ingredient, name='delete_ingredient'),

    # Categories (MainMenu)
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
]
