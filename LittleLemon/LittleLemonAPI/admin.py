from django.contrib import admin
from .models import Cart, MenuItem, Order, OrderItem
# Register your models here.
admin.site.register(Cart)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)