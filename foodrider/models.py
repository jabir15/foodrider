from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import format
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return str(self.id) + '--' + self.name
    
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    rating = models.IntegerField(
        default=3, null=True, blank=True,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
     )
    def __str__(self):
        return self.name

    @property
    def get_menu_items(self):
        return self.menuitem_set.all()

class MenuItem(models.Model):
    name = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)

    @property
    def get_all_options(self):
        return self.menuitemoption_set.all()

    def __str__(self):
        return self.restaurant.name + '-' + self.name

class MenuItemOption(models.Model):
    CHOICES = [('VEG', 'Veg'), ('NVG', 'Non-Veg')]
    DISHES = [('S', 'Starters'), ('M', 'Main Course'), ('D', 'Desserts')]
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    item_type = models.CharField(max_length=3, choices=CHOICES, default='VEG')
    dish_type = models.CharField(max_length=1, choices=DISHES, default='M')
    nominal_price = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0.00))
    discount_price = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(0.00))

    @property
    def get_actual_price(self):
        actual_price = self.nominal_price - self.discount_price
        return actual_price
        
    def __str__(self):
        return (str(self.id) + (' ' if self.discount_price.is_zero() else ' *Discount* ') 
                + self.menu.restaurant.name + '--'
                + self.menu.name + '--'
                + self.name + '--' + str(self.nominal_price)
            )

class Order(models.Model):
    # https://www.youtube.com/watch?v=obZMr9URmVI
    ORDER_STATUS = [
        (1, 'Placed'),
        (2, 'Confirmed'),
        (3, 'Ready'),
        (4, 'Picked Up'),
        (5, 'Delivered')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUS, default=1)
    date_picked = models.DateTimeField(blank = True, null = True)
    driver = models.ForeignKey('DriverDetail', on_delete=models.SET_NULL, null=True, blank=True)
    date_delivered = models.DateTimeField(blank=True, null=True)
    transaction_id = models.CharField(max_length=15, null=True, blank=True, editable=True, unique=True)
    razor_order_id = models.CharField(max_length=30, null=True, blank=True, unique=True)
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True, blank=True)
    delivery_charge = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal(39.00))

    @property
    def get_cart_total_nominal_price(self):
        orderitems = self.orderdetail_set.all()
        total = sum([item.get_nominal_price_times_quantity for item in orderitems])
        return total
    
    @property
    def get_cart_total_actual_price_without_delivery(self):
        orderitems = self.orderdetail_set.all()
        total = sum([item.get_actual_price_times_quantity for item in orderitems])
        return total

    @property
    def get_cart_total_actual_price(self):
        orderitems = self.orderdetail_set.all()
        total = sum([item.get_actual_price_times_quantity for item in orderitems])
        return total + self.delivery_charge
    
    @property
    def get_cart_total_price_with_trans(self):
        base_amount = int(self.get_cart_total_actual_price*100)
        charge = int(base_amount*0.02)
        return {'price':(base_amount + charge)/100, 'charge':charge/100}


    @property
    def get_cart_total_discount_price(self):
        orderitems = self.orderdetail_set.all()
        total = sum([item.get_discount_price_times_quantity for item in orderitems])
        return total

    @property
    def get_cart_total_items(self):
        orderitems = self.orderdetail_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.id) + '--' + self.transaction_id + '--' + self.get_status_display()

class OrderDetail(models.Model):
    menu_item = models.ForeignKey(MenuItemOption, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_actual_price_times_quantity(self):
        total_price = self.menu_item.get_actual_price * self.quantity
        return total_price
    
    @property
    def get_nominal_price_times_quantity(self):
        total_price = self.menu_item.nominal_price * self.quantity
        return total_price
    
    @property
    def get_discount_price_times_quantity(self):
        total_price = self.menu_item.discount_price * self.quantity
        return total_price
    
    def __str__(self):
        return str(self.order.id) + '--' + self.menu_item.__str__() + ' x ' + str(self.quantity)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    # city = models.CharField(max_length=200, default='Silchar')
    # state = models.CharField(max_length=200, default='Assam')
    # pincode = models.CharField(max_length=200, default='788001')
    date_added = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(null=True, blank=True, default=False)
    phone_number = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Shipping Addresses'
    
    def __str__(self):
        return self.customer.name + '--' + self.address

class DriverDetail(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    