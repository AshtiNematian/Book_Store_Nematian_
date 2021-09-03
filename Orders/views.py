from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from User.models import Address
from Basket.models import Basket, basket
from Orders.models import Order, ItemOrder
from Orders.forms import OrderForm
from django.contrib import messages


def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return orders


def order_view(request):
    basket = Basket(request)
    basket_total = basket.get_total_price()
    user = request.user
    form = OrderForm()

    if request.method == 'POST':
        data = request.POST

        orderAddress = Address.objects.get(id=data['address'])

        order = Order.objects.create(full_name=data['full_name'], email=data['email'], phone=data['phone'],
                                     address_line1=data['address_line1'],
                                     town_city=data['town_city'], address=orderAddress,
                                     post_code=data['post_code'], user=user, paid=True, total_paid=basket_total)

        for item in basket:
            ItemOrder.objects.create(user=user, order=order, product=item['product'], quantity=item['qty'])

        order.save()
        messages.success(request, 'سفارش شما با موفقیت ثبت شد')
    order = Order.objects.all()
    context = {'order': order, 'form': form}
    return render(request, 'paid.html', context)


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'orderplaced.html')


class Error(TemplateView):
    template_name = 'error.html'
