from django.urls import path

from Orders import views

app_name = 'order'
urlpatterns = [
    path('pay/', views.order_view, name='order_view'),
    path('error/', views.Error.as_view(), name='error'),
    path('order_placed/', views.order_placed, name='order_placed')

]
