from django.urls import path
from . import views

urlpatterns = [
    path('reservedTables/', views.reserved_tables, name='reserved_tables'),
    path('update_reservation/<int:pk>/', views.update_reservation, name='update_reservation'),
    path('cancel_reservation/<int:pk>/', views.cancel_reservation, name='delete_reservation'),
]  