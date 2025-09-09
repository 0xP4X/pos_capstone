from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'low_stock')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'barcode')
    ordering = ('name',)
    # yo these fields are grouped nicely
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'description', 'barcode')
        }),
        ('Stock & Pricing', {
            'fields': ('price', 'stock_quantity', 'minimum_stock')
        }),
    )
