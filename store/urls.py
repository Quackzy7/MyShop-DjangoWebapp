from django.contrib import admin
from django.urls import path,include
from store.views import *

urlpatterns = [
    path('products/',display_products,name='products'),
    path('products/<slug:slug>-<int:id>/',product_detail, name='product_detail'),
    path('signup/buyer/', buyer_signup, name='buyer_signup'),
    path('signup/seller/', seller_signup, name='seller_signup'),
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller/add/', add_product, name='add_product'),
    path('seller/edit/<int:id>/', update_product, name='update_product'),
    path('seller/delete/<int:id>/', delete_product, name='delete_product'),
]
