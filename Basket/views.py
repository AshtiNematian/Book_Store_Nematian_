from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from Basket.models import Basket
from Coupon.forms import CouponApplyForm
from Product.models import Book


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Book, id=product_id)
        basket.add(product=product, qty=product_qty)
        coupon_apply_forms = CouponApplyForm()
        if product.inventory != 0 and product_qty < product.inventory:
            basket.add(product=product, qty=product_qty)
            product.remove_items_from_inventory(product_qty)
        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty,
                                 'subtotal': baskettotal})
        return response
