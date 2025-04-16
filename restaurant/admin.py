from django.contrib import admin
from .models import Restaurant, Manager, Chef, Server, DeliveryPerson

admin.site.register(Restaurant)
admin.site.register(Manager)
admin.site.register(Chef)
admin.site.register(Server)
admin.site.register(DeliveryPerson)
