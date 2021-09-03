from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Product.urls', namespace='store')),
    path('basket/', include('Basket.urls', namespace='basket')),
    path('account/', include('User.urls', namespace='account')),
    path('orders/', include('Orders.urls', namespace='orders')),
    path('coupon/', include('Coupon.urls', namespace='coupons')),
    path('', include('adminlte_full.urls'))
    # path('payment/', include('Payment.urls', namespace='payment')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
