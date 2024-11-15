from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import (
    Index, About, Order, OrderConfirmation, OrderPayConfirmation,
    Menu, MenuSearch, GetStarted, weblogin, websigin, feedback_view,
    login_selection, add_to_cart, view_cart, clear_cart, RestaurantListView,
    RestaurantDetailView, new_order_confirmation, OrderSuccessView, order_summary, get_order_status
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('restaurant/', include('restaurant.urls')),

    # Feedback page
    path('feedback/', feedback_view, name='feedback'),

    # Get Started page
    path('', GetStarted.as_view(), name='get-started'),
    path('customadmin/', include('customadmin.urls')),

    # Login and Signup views
    path('weblogin/', weblogin.as_view(), name='weblogin'),
    path('websigin/', websigin.as_view(), name='websigin'),
    path('login-selection/', login_selection, name='login_selection'),

    # Menu and cart views
    path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),  # Correctly refer to the view
    path('cart/', view_cart, name='view_cart'),  # Correctly refer to the view
    path('cart/clear/', clear_cart, name='clear_cart'),

    path('index/', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('menu/', Menu.as_view(), name='menu'),
    path('menu/search/', MenuSearch.as_view(), name='menu-search'),
    path('get_order_status/', get_order_status, name='get_order_status'),

    # Order views
    path('order/', Order.as_view(), name='order'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-confirmation'),
    path('order-success/', OrderSuccessView.as_view(), name='order_success'),
    path('order-summary/', order_summary, name='order_summary'),

    # Restaurant views
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurants/<int:restaurant_id>/', RestaurantDetailView.as_view(), name='restaurant_detail'),  # Basic restaurant view
    path('restaurants/<int:restaurant_id>/menu_item/<int:menu_item_id>/', RestaurantDetailView.as_view(), name='restaurant_detail_with_item'),
    path('restaurants/<int:restaurant_id>/menu-item/<int:menu_item_id>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('order-confirmation/<int:order_id>/', new_order_confirmation, name='new_order_confirmation'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
