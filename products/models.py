from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # Ensure price is positive
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # yo this will help track if stock is running low
    minimum_stock = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    @property
    def low_stock(self):
        # returns True if stock is below minimum_stock
        return self.stock_quantity <= self.minimum_stock
