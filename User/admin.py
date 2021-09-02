from django.contrib import admin
from User.models import UserBase, Address


@admin.register(UserBase)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "user_name", 'mobile', 'is_active', 'created', 'is_staff')
    search_fields = ['mobile']
    list_filter = ['is_staff']
    ordering = ('id', 'created')
    empty_value_display = '-empty-'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("customer", "full_name", 'phone', 'town_city')
    search_fields = ['full_name']
    ordering = ('town_city',)
