from django.contrib import admin
from .models import Product, ProductsImage, OrderItem, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price')
    search_fields = ('title', 'description', 'category', 'brand', 'slug')
    list_filter = ('brand', 'category')
    prepopulated_fields = {'slug': ('title', 'brand', 'category')}


@admin.register(ProductsImage)
class ProductsImage(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product',)


admin.site.register(Order)
admin.site.register(OrderItem)
