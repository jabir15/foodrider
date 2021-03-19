from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from foodrider.models import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from foodrider.utils import checkOrder
import datetime
import time

# Create your views here.

def registerOrLogin(request):
    if request.method=='POST':
        if 'sign-up' in request.POST:
            loginform = AuthenticationForm()
            signupform = CustomUserCreationForm(request.POST)
            if signupform.is_valid():
                signupform.save()
                username = signupform.cleaned_data.get('username')
                raw_password = signupform.cleaned_data.get('password1')
                user = authenticate(username=username,password=raw_password)
                login(request,user)
                return redirect(request.GET.get('next','index'))

        if 'log-in' in request.POST:
            signupform = CustomUserCreationForm()
            loginform = AuthenticationForm(data=request.POST)
            if loginform.is_valid():
                user = loginform.get_user()
                login(request,user)
                return redirect(request.GET.get('next','index'))
        
    else:
        signupform = CustomUserCreationForm()
        loginform = AuthenticationForm()
    redirecturl = request.GET.get('next', 'index')    
    return render(request, 'users/register.html', {'signupform':signupform, 'loginform':loginform, 'tab':redirecturl})
    # return render(request, 'users/register_x.html')

def username_check(user):
    return user.username == 'foodrider_admin'

@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
def adminDashboard(request):
    number_of_menuitems = MenuItem.objects.all().count()
    number_of_orders = Order.objects.all().count()
    number_of_customers = Customer.objects.all().count()
    context = {
        'number_of_menuitems':number_of_menuitems,
        'number_of_orders':number_of_orders,
        'number_of_customers':number_of_customers
    }
    return render(request, 'users/admin-dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
def adminDashboardProducts(request):
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants,
        'selected_restaurant': 'None'
    }
    
    return render(request, 'users/admin-dashboard-products.html', context)

@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
@require_http_methods(["POST"])
def get_menus_by_restaurant(request):
    restaurant_name = request.POST.get('restaurant_name', '')
    if restaurant_name == 'R00':
        menus = MenuItem.objects.none()
    else:
        menus = MenuItem.objects.filter(restaurant__name=restaurant_name)
    context = {'menus': menus}
    return render(request, 'users/includes/menu-by-restaurant.html', context)

@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
@require_http_methods(["POST"])
def get_menuoptions_by_menu(request):
    restaurant_name = request.POST.get('restaurant_name', '')
    menu_name = request.POST.get('menu_name', '')
    if menu_name == "M00":
        menuoptions = MenuItemOption.objects.none()
    else:
        menuoptions = MenuItemOption.objects.filter(menu__name=menu_name, menu__restaurant__name=restaurant_name)
    context = {'menuoptions':menuoptions}

    return render(request, 'users/includes/menuoption-by-menu.html', context)

@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
@require_http_methods(["POST"])
def create_or_update_menu_option(request):
    restaurant_name = request.POST.get('restaurant_name', '')
    menu_name = request.POST.get('menu_name', '')
    menu_option_id = request.POST.get('menu_option_id', '')
    menu_option_name = request.POST.get('menu_option_name', '')
    menu_option_item = request.POST.get('menu_option_item', '')
    menu_option_dish = request.POST.get('menu_option_dish', '')
    menu_option_np = request.POST.get('menu_option_nominal_price', '0.00')
    menu_option_dp = request.POST.get('menu_option_discount_price', '0.00')
    action = request.POST.get('action', '')

    restaurant = Restaurant.objects.get(name=restaurant_name)
    menuitem = MenuItem.objects.get(name=menu_name, restaurant=restaurant)

    if action == 'delete':
        MenuItemOption.objects.filter(id=menu_option_id[7:]).delete()
        # data = {}
    elif action == 'update':
        MenuItemOption.objects.filter(id=menu_option_id[7:]).update(
            name = menu_option_name,
            item_type = menu_option_item,
            dish_type = menu_option_dish,
            nominal_price = Decimal(menu_option_np.strip() or 0),
            discount_price = Decimal(menu_option_dp.strip() or 0)
        )
    else:
        MenuItemOption.objects.create(
            menu = menuitem,
            name = menu_option_name,
            item_type = menu_option_item,
            dish_type = menu_option_dish,
            nominal_price = Decimal(menu_option_np.strip() or 0),
            discount_price = Decimal(menu_option_dp.strip() or 0)
        )
    
    data = get_menuoptions_by_menu(request)

    return HttpResponse(data)


@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
def adminDashboardOrders(request):
    orders = Order.objects.all().order_by('-date_ordered', 'status')
    context = {'orders': orders}
    return render(request, 'users/admin-dashboard-orders.html', context)
    
@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
def adminDashboardOrderDetails(request, transactionid):
    if request.method == 'POST':
        print(request.POST)
        status = request.POST.get('order_status')
        driver_name = request.POST.get('driver_name')
        driver_ph_nu = request.POST.get('driver_phone_number')
        date_pickup = request.POST.get('pickup-time')
        date_delivered = request.POST.get('delivery-time')
        
        order = Order.objects.get(transaction_id=transactionid)
        order.status = int(status)

        if driver_name and driver_ph_nu:
            driver, ctd = DriverDetail.objects.get_or_create(name=driver_name, phone_number=driver_ph_nu)
            order.driver = driver
        if date_pickup:
            order.date_picked = date_pickup
        if date_delivered:
            order.date_delivered = date_delivered 

        order.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        context = checkOrder(transactionid)
        context['drivers'] = DriverDetail.objects.all()
        return render(request, 'users/order-details.html', context )

@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
@require_http_methods(["POST"])
def addNewRestaurant(request):
    res_name = request.POST.get('restaurant_name_new')
    Restaurant.objects.create(name=res_name)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
@require_http_methods(["POST"])
def addNewMenuItem(request):
    menu_name = request.POST.get('menu_name_new')
    res_name = request.POST.get('select-restaurant')
    restaurant = Restaurant.objects.get(name=res_name)
    MenuItem.objects.create(name=menu_name, restaurant=restaurant)
    
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants,
        'selected_restaurant': res_name,
    } 
    return render(request, 'users/admin-dashboard-products.html', context)

@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
def adminDashboardCustomers(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, 'users/admin-dashboard-customers.html', context)

@login_required(login_url='login')
@user_passes_test(username_check, login_url='login')
def adminDashboardCustomerDetails(request, cid):
    customer = Customer.objects.get(id=cid)
    orders = customer.order_set.all()
    context = {
        'customer':customer,
        'orders':orders
    }
    return render(request, 'users/customer-details.html',context)
