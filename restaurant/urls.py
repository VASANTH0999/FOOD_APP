from django.urls import path
from .views import Dashboard, OrderDetails, custom_403_view
from django.conf.urls import handler403

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('orders/<int:pk>/', OrderDetails.as_view(), name='order-details'),
]


handler403 = custom_403_view
