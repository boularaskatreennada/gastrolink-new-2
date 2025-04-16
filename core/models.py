from django.db import models

class PDG(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    loyalityPoints = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} "
