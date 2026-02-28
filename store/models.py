
from django.db import models
from django.utils.text import slugify
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField(default=0)
    description=models.TextField(blank=True,null=True)
    slug = models.SlugField(blank=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    
