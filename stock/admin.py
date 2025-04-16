from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'ingredient', 'quantity', 'min_threshold', 'expiry_date')
    list_filter = ('restaurant', 'ingredient')