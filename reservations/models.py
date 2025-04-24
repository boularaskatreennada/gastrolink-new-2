from django.db import models
from restaurant.models import *

class TableStatus(models.TextChoices):
    FREE = 'free', 'Free'
    OCCUPIED = 'not_free', 'Occupied'

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=15, choices=TableStatus.choices)

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    number_of_people = models.PositiveIntegerField()
    status = models.CharField(max_length=20)