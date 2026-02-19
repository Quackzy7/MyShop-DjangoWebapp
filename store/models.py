from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.


    


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES=(
        ('buyer','Buyer'),
        ('seller','Seller'),
    )

    user_type=models.CharField(max_length=10,choices=USER_TYPE_CHOICES,default='buyer')

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
    phone_number = models.CharField(max_length=15)

class Product(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField(default=0)
    description=models.TextField(blank=True,null=True)
    slug = models.SlugField(blank=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name