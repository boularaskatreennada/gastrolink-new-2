from django.db import models
from restaurant.models import Restaurant

class Expense(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    expense_date = models.DateField()
