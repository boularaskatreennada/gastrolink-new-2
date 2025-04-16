from django.db import models
from restaurant.models import Restaurant
from menu.models import Ingredient
# Create your models here.
class Stock(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    min_threshold = models.FloatField()
    expiry_date = models.DateField()