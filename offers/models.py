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
    uses = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=OfferStatus.choices)

    def __str__(self):
        return self.title