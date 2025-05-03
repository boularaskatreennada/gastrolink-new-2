from django.db import models
from reservations.models import Table
from restaurant.models import *
from menu.models import Dish


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PREPARING = 'preparing', 'Preparing'
    DONE = 'done', 'Done'
    CANCELLED='cancelled','Cancelled'

class OrderMode(models.TextChoices):
    SERVED = 'served', 'Served'
    DELIVERED = 'delivered', 'Delivered'

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=OrderStatus.choices)
    mode = models.CharField(max_length=10, choices=OrderMode.choices)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True,blank=True)
    server = models.ForeignKey(Server, on_delete=models.SET_NULL, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table  = models.ForeignKey(Table,on_delete=models.SET_NULL, null=True,  blank=True )

class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order', 'dish')

class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_person = models.ForeignKey(DeliveryPerson, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField()
    status = models.CharField(max_length=50)
