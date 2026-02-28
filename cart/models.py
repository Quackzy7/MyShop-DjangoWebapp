from django.db import models
from django.conf import settings
from store.models import Product
# Create your models here.
class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="cart")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.name}"
    
    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")

    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="cartitem")
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"CartItem - {self.product.name}x{self.quantity}"
    
    def total_price(self):
        return self.quantity * self.product.price