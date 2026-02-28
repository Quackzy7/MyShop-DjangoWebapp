
from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('products/',display_products,name='products'),
    path('products/<slug:slug>-<int:id>/',product_detail, name='product_detail'),
    
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller/add/', add_product, name='add_product'),
    path('seller/edit/<int:id>/', update_product, name='update_product'),
    path('seller/delete/<int:id>/', delete_product, name='delete_product'),
]
