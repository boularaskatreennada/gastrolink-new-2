from django.db import models

class OfferStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    UPCOMING = 'upcoming', 'Upcoming'
    EXPIRED = 'expired', 'Expired'

class Offer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    discount = models.FloatField()
    code = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=OfferStatus.choices)