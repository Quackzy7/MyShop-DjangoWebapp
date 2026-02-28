
from django.urls import path
from .views import *

urlpatterns = [
   path('',cart_detail,name='cart_detail'),
   path("add/<int:id>/",add_to_cart , name="add_to_cart"),
   path('cart/remove/<int:id>/', remove_from_cart, name='remove_from_cart'),
]
