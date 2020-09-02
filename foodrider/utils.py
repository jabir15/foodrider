import json
from .models import *

def cookieCart(request):
    cart = json.loads(request.COOKIES['cart'])
    # print('Cart:',cart)
    order = {
        'get_cart_total_items': 0,
        'get_cart_total_actual_price_without_delivery': 0,
        'get_cart_total_nominal_price':0,
        'get_cart_total_discount_price':0,
        'get_cart_total_actual_price':0,
        'delivery_charge':Decimal(0.00)
    }
    order_items = []
    for i in cart:
        menu_item = MenuItemOption.objects.get(id=int(i))
        order['get_cart_total_items'] += cart[i]["quantity"]
        order['get_cart_total_actual_price_without_delivery'] += menu_item.nominal_price * cart[i]["quantity"]
        order['get_cart_total_nominal_price'] += menu_item.nominal_price * cart[i]["quantity"]
        order['get_cart_total_discount_price'] += menu_item.discount_price * cart[i]["quantity"]
        order['get_cart_total_actual_price'] += menu_item.get_actual_price * cart[i]["quantity"]
        order['delivery_charge'] = Decimal(39.00)

        item = {
            'menu_item': menu_item,
            'quantity': cart[i]["quantity"],
            'get_actual_price_times_quantity': menu_item.get_actual_price * cart[i]["quantity"],
            'get_nominal_price_times_quantity': menu_item.nominal_price * cart[i]["quantity"],
            'get_discount_price_times_quantity': menu_item.discount_price * cart[i]["quantity"]
        }
        order_items.append(item)
    order['get_cart_total_actual_price'] += order['delivery_charge']

    return {'order_items': order_items, 'order': order}

def cartData(request):
    cookieData = cookieCart(request)
    order_items = cookieData['order_items']
    order = cookieData['order']

    return {'order_items': order_items, 'order': order}

def checkOrder(transactionid):
    try:
        order = Order.objects.get(transaction_id=transactionid)
        order_items = order.orderdetail_set.all()
        restaurant = order_items[0].menu_item.menu.restaurant.name
        context = {
            'found':'true',
            'order':order,
            'order_items':order_items,
            'restaurant': restaurant,
        }
    except Order.DoesNotExist:
        context = {'found':'false'}

    return context

