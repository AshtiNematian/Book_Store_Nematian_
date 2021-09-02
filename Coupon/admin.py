

from django.contrib import admin

from Coupon.models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "active")
    search_fields = ['code']
    list_filter = ['active']
    ordering = ('id', 'valid_from')
