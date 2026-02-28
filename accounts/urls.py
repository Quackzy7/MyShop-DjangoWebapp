
from django.urls import path
from .views import *

urlpatterns = [
    path('signup/buyer/', buyer_signup, name='buyer_signup'),
    path('signup/seller/', seller_signup, name='seller_signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
 
]
