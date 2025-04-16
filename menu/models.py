from django.db import models
from restaurant.models import Restaurant

class MainMenu(models.Model):
    category = models.CharField(max_length=100)

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='dishes/')
    menu = models.ForeignKey(MainMenu, on_delete=models.CASCADE)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()

    class Meta:
        unique_together = ('dish', 'ingredient')

class DailyMenu(models.Model):
    date = models.DateField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class DailyMenuDish(models.Model):
    menu = models.ForeignKey(DailyMenu, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    available_quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('menu', 'dish')
