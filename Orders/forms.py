from django.forms import ModelForm

from Orders.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [ 'email','full_name', 'address','address_line1','post_code','phone','town_city']
