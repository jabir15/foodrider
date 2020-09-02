from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(MenuItemOption)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(ShippingAddress)
admin.site.register(DriverDetail)
# Register your models here.
