from django.db import models
from Product.models import Book
from User.models import UserBase, Address


class Order(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    total_paid = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    address_line1 = models.CharField(max_length=250, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, null=True, blank=True)
    town_city = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سفارش   "
        verbose_name_plural = "سفارش ها"
        ordering = ('-created',)

    def __str__(self):
        return str(self.user.user_name)


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_item')
    user = models.ForeignKey(UserBase, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "جزییات سفارش  "
        verbose_name_plural = "جزییات سفارش ها "

    def __str__(self):
        return self.user.user_name
