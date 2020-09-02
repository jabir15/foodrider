from django.urls import path
from . import views

urlpatterns = [
    path('restaurant-list/<int:id>/', views.product_details, name='restaurant-details'),
    path('restaurant-list/', views.restaurant_list, name='restaurant-list'),
    path('cart/', views.cart, name='cart'),
    path('cart-summary/', views.get_cart_summary, name='cart-summary'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-placed/', views.orderPlaced, name='order-placed'),
    path('order-confirmed/<str:transactionid>/', views.orderConfirmed, name='order-confirmed'),
    path('payment-success/', views.paymentSuccess, name='payment-success'),
    path('customer-address/', views.get_shippingaddresses_by_customer, name='customer-address'),
    path('create-or-update-address/', views.create_or_update_address, name='create-or-update-address'),
    path('before-checkout/', views.beforeCheckout, name='before-checkout'),
    path('your-orders/', views.yourOrders, name='your-orders'),
    path('track-orders/', views.trackOrders, name='track-orders'),
    path('', views.index, name='index'),
]
