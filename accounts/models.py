from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES=(
        ('buyer','Buyer'),
        ('seller','Seller'),
    )
    user_type=models.CharField(max_length=10,choices=USER_TYPE_CHOICES,default='buyer')
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'
    def is_seller(self):
        return self.user_type=='seller'

    def is_buyer(self):
        return self.user_type=='buyer'
    
class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=20)

class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    shipping_address = models.TextField()