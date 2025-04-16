from django.contrib import admin
from .models import Offer

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'discount', 'code', 'status')
    list_filter = ('status',)
    search_fields = ('code', 'title')