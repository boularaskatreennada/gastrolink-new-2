from django.urls import path
from . import views

urlpatterns = [
   path('manager/orders/', views.orders_list, name='clients_orders_list'),
] 