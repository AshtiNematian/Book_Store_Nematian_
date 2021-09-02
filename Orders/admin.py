from django.contrib import admin
from Orders.models import Order, ItemOrder


@admin.register(ItemOrder)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('user', "product", 'quantity', 'order')
    search_fields = ['product']
    list_filter = ['quantity']
    ordering = ('id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", 'created', 'paid')
    search_fields = ['user']
    list_filter = ['created']
    ordering = ('id', 'created')
