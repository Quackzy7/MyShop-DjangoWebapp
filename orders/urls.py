from django.urls import path
from .views import *

urlpatterns = [
path('', order_list, name='order_list'),
path('checkout/', checkout, name='checkout'),
path('<int:order_id>/', order_detail, name='order_detail'),
path("seller/items/", seller_order_items, name="seller_order_items"),
path("seller/items/<int:item_id>/",update_order_item, name="update_order_item"),
path("stripe-success/", stripe_success, name="stripe_success"),
]
