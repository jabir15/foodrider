from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import BadHeaderError, EmailMessage
from django.template.loader import get_template
import json
from foodrider.models import *
from .utils import cookieCart, cartData, checkOrder
from decimal import Decimal
from django.utils.crypto import get_random_string
from users.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.conf import settings

import razorpay
client = razorpay.Client(auth=(settings.RAZORPAY_API, settings.RAZORPAY_SECRET))

# Create your views here.
def index(request):
    return render(request, 'foodrider/index.html')

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    context = {'restaurants': restaurants}
    return render(request, 'foodrider/restaurant-list.html', context)

def product_details(request,id):
    restaurant = Restaurant.objects.get(pk=id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    
    data = cartData(request)
    order_items = data['order_items']
    order = data['order']

    context = {
        'cart_items': order_items,
        'order':order,
        'restaurant': restaurant,
        'menu_items': menu_items
    }
    return render(request, 'foodrider/product-details.html', context)

def cart(request):
    data = cartData(request)
    order_items = data['order_items']
    order = data['order']
           
    context = {'cart_items': order_items, 'order':order}
    return render(request, 'foodrider/cart.html', context)

def get_cart_summary(request):
    data = cartData(request)
    order_items = data['order_items']
    order = data['order']
           
    context = {'cart_items': order_items, 'order':order}
    return render(request, 'foodrider/includes/cart-summary.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        name = customer.name
        email = customer.email
        # address = customer.shippingaddress_set.all()[0]
        try:
            sh_address = ShippingAddress.objects.filter(customer=customer).get(is_default=True)
        except:
            address = ''
            phone = ''
        else:
            address = sh_address.address
            phone = sh_address.phone_number

        formdata = {
            'fname':name.strip().split(' ')[0],
            'lname':' '.join(name.strip().split(' ')[1:]),
            'email':email,
            'address':address,
            'phone':phone,
        }
    else:
        formdata = {}
    
    data = cartData(request)
    order_items = data['order_items']
    order = data['order']

    context = {'cart_items': order_items, 'order':order, 'formdata':formdata}
    return render(request, 'foodrider/checkout.html', context)

@require_http_methods(["POST"])
def orderPlaced(request):
    # data = json.loads(request.body)
    form_data = request.POST
    
    if request.user.is_authenticated:
        customer = request.user.customer

    else:
        customer, created = Customer.objects.get_or_create(
            name=form_data['fname']+' '+form_data['lname'],
            email=form_data['email']
        )
    # Create order and update it with the cart 
    order = Order.objects.create(
            customer=customer,
            status=1,
            transaction_id=get_random_string(length=15)
        )
    cart = json.loads(request.COOKIES['cart'])

    for i in cart:
        menu_item = MenuItemOption.objects.get(id=int(i))
        order_detail = OrderDetail.objects.create(
            menu_item=menu_item,
            order=order,
            quantity=cart[i]['quantity'])
    
    # Create shipping address of the customer
    shipping, created = ShippingAddress.objects.get_or_create(
            customer=customer,
            address=form_data['address'],
            phone_number=form_data['phone']
        )
    shipping.is_default = form_data.get('make_default','')=='on'
    shipping.save()
    order.shipping_address = shipping
    order.save()

    base_amount = int(order.get_cart_total_actual_price*100)
    trans_charge = base_amount*0.02
    amount = base_amount + trans_charge
    if form_data['paymentmethods'] == 'ONL':
        r_data = {
            'amount': int(amount),
            'currency':'INR',
            'receipt': get_random_string(length=6),
            'payment_capture':1,
        }
        razor_order = client.order.create(r_data)
        order.razor_order_id = razor_order['id']
        order.save()
        order_items = order.orderdetail_set.all()
        formdata = {
            'fname': shipping.customer.name.strip().split(' ')[0],
            'lname':' '.join(shipping.customer.name.strip().split(' ')[1:]),
            'email':shipping.customer.email,
            'address':shipping.address,
            'phone':shipping.phone_number,
        }
        context = {
            'cart_items': order_items,
            'order':order,
            'formdata':formdata,
            'razor_order':razor_order,
            'prefill_name':customer.name, 
            'prefill_email':customer.email, 
            'prefill_contact':shipping.phone_number, 
        }
        return render(request, 'foodrider/checkout.html', context)
    else:
        return redirect('order-confirmed', transactionid=order.transaction_id)

def orderConfirmed(request, transactionid):
    context = checkOrder(transactionid)
    response = render(request, 'foodrider/track-orders.html', context )
    
    subject = f'Order Confirmation for ID-{transactionid}'
    content = get_template('foodrider/includes/order-items.html').render(context)
    from_email = 'assamcollegecode.pythonanywhere@gmail.com'
    to_email = context['order'].customer.email
    email = EmailMessage(subject, content, from_email, [to_email])
    email.content_subtype = 'html'
    email.send()
    response.delete_cookie('cart')
    return response

def beforeCheckout(request):

    if request.user.is_authenticated:
        response = redirect('checkout')
    else:
        signupform = CustomUserCreationForm()
        loginform = AuthenticationForm()
        redirecturl = 'checkout'

        response =  render(request, 'users/register.html', {'signupform':signupform, 'loginform':loginform, 'tab':'checkout'})

    return response

@login_required(login_url='login')
def yourOrders(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer).order_by('status', '-date_ordered')
    shipping_addresses = ShippingAddress.objects.filter(customer=customer).order_by('-is_default')
    context = {'orders': orders, 'shippings':shipping_addresses}
    return render(request, 'foodrider/your-orders.html', context)
    
def trackOrders(request):
    if request.method=='POST':
        transactionid = request.POST.get('transactionid')
        context = checkOrder(transactionid)
    else:
        context = {}

    return render(request, 'foodrider/track-orders.html', context)

@login_required(login_url='login')
@require_http_methods(["POST"])
def get_shippingaddresses_by_customer(request):
    customer = request.user.customer
    shippings = ShippingAddress.objects.filter(customer=customer).order_by('-is_default')
    context = {
        'shippings':shippings,
    }
    return render(request, 'foodrider/includes/customer_address.html', context)

@login_required(login_url='login')
@require_http_methods(["POST"])
def create_or_update_address(request):
    customer = request.user.customer
    action = request.POST.get('action', '')
    value = request.POST.get('update_value', '')
    ship_id = request.POST.get('shipping_id', '')

    street = request.POST.get('street', '')
    phone = request.POST.get('phone', '')
    makedef = request.POST.get('make_default', '')

    try:
        shipping_address = ShippingAddress.objects.get(id=ship_id)
    except:
        shipping_address = ShippingAddress.objects.create(
            customer=customer,
            address=street,
            phone_number = phone,
        )
        if makedef == 'true':
            shipping_address.is_default = True
            oth_ships = ShippingAddress.objects.filter(customer=customer).exclude(id=shipping_address.id)
            for oth_ship in oth_ships:
                oth_ship.is_default = False
                oth_ship.save()
    
    if action == 'update-address':
        shipping_address.address = value
    elif action == 'update-phone':
        shipping_address.phone_number = value
    elif action == 'update-default':
        shipping_address.is_default = True
        oth_ships = ShippingAddress.objects.exclude(id=ship_id)
        for oth_ship in oth_ships:
            oth_ship.is_default = False
            oth_ship.save()
    
    elif action == 'delete':
        shipping_address.delete()
        return HttpResponse(get_shippingaddresses_by_customer(request))
        
    shipping_address.save()
    data = get_shippingaddresses_by_customer(request)
    return HttpResponse(data)



@require_http_methods(["POST"])
def paymentSuccess(request):
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    razorpay_order_id = request.POST.get('razorpay_order_id', '')
    razorpay_signature = request.POST.get('razorpay_signature', '')
    try:
        params_dict = {
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_signature': razorpay_signature
        }
        client.utility.verify_payment_signature(params_dict)
    except razorpay.errors.SignatureVerificationError:
        return HttpResponse('Payment failed, please try again later')
    else:
        order = Order.objects.get(razor_order_id=razorpay_order_id)
        order.status = 2
        order.save()
        return redirect('order-confirmed', transactionid=order.transaction_id)
