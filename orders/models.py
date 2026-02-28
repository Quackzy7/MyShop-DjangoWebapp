from django.db import models
from django.conf import settings
from store.models import Product
# Create your models here.
class Order(models.Model):
    OVERALL_STATUS = (
        ('pending', 'Pending'),
        ("processing", "Processing"),
        ("partially_shipped", "Partially Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    )
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="orders")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    overall_status = models.CharField(max_length=30, choices=OVERALL_STATUS, default="pending")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    def update_overall_status(self):
        items = self.items.all()

        if all(item.status == "cancelled" for item in items):
            self.overall_status = "cancelled"
        elif all(item.status == "delivered" for item in items):
            self.overall_status = "completed"
        elif any(item.status == "shipped" for item in items):
            self.overall_status = "partially_shipped"
        elif any(item.status == "processing" for item in items):
            self.overall_status = "processing"
        else:
            self.overall_status = "pending"

        self.save()
    
class OrderItem(models.Model):
    STATUS_CHOICES= (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(default=1)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def total_price(self):
        return self.price * self.quantity
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.update_overall_status()
    
class Payment(models.Model):

    PAYMENT_METHOD_CHOICES = (
        ("stripe", "Stripe"),
        ("cod", "Cash On Delivery"),
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    )

    order = models.OneToOneField(
        "Order",
        on_delete=models.CASCADE,
        related_name="payment"
    )

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=255, blank=True, null=True,unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
    