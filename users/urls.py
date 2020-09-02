from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('login/<str:redirecturl>', views.registerOrLogin, name='login'),
    path('login/', views.registerOrLogin, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin-dashboard/', views.adminDashboard, name='admin-dashboard'),
    path('admin-dashboard-products/', views.adminDashboardProducts, name='admin-dashboard-products'),
    path('admin-dashboard-orders/', views.adminDashboardOrders, name='admin-dashboard-orders'),
    path('admin-dashboard-orders/<str:transactionid>/', views.adminDashboardOrderDetails, name='admin-order-details'),
    path('menu-by-restaurant/', views.get_menus_by_restaurant, name='menu-by-restaurant'),
    path('menuoption-by-menu/', views.get_menuoptions_by_menu, name='menuoption-by-menu'),
    path('create-or-update-menu-option/', views.create_or_update_menu_option, name='create-or-update-menu-option'),
    path('add-restaurant/', views.addNewRestaurant, name='add-restaurant'),
    path('add-menu-item/', views.addNewMenuItem, name='add-menu-item'),

    path('admin-dashboard-customers/', views.adminDashboardCustomers, name='admin-dashboard-customers'),
    path('admin-dashboard-customers/<str:cid>/', views.adminDashboardCustomerDetails, name='admin-customer-details'),

]
