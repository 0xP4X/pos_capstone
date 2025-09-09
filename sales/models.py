from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product
from django.contrib.auth import get_user_model

class Sale(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('MOBILE', 'Mobile Payment'),
    ]
    
    cashier = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='CASH')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # yo adding some useful stuff for tracking payments
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    change_given = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Sale #{self.id} - ${self.total_amount}"
    
    @property
    def get_change(self):
        return self.amount_paid - self.total_amount

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at time of sale
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name if self.product else 'Deleted Product'}"
    
    def save(self, *args, **kwargs):
        # Store the current price if not already set
        if not self.price_at_sale:
            self.price_at_sale = self.product.price
        super().save(*args, **kwargs)
