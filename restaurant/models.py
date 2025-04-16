from django.db import models

class EmployeeStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Manager(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    created_at = models.DateField()
    status = models.CharField(max_length=10, choices=EmployeeStatus.choices)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Chef(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    created_at = models.DateField()
    status = models.CharField(max_length=10, choices=EmployeeStatus.choices)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class Server(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    created_at = models.DateField()
    status = models.CharField(max_length=10, choices=EmployeeStatus.choices)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class DeliveryPerson(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    created_at = models.DateField()
    status = models.CharField(max_length=10, choices=EmployeeStatus.choices)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
