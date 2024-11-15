from allauth.account.views import LogoutView
from django.urls import path
from . import views
from .views import admin_login

app_name = 'customadmin'
urlpatterns = [
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('restaurants/', views.restaurant_list, name='restaurant_list'),
    path('view_selected_items/', views.view_selected_items, name='view_selected_items'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('order/review/', views.order_review, name='order_review'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
