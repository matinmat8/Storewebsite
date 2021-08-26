from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price')
    search_fields = ('title', 'description', 'category', 'brand', 'slug')
    list_filter = ('brand', 'category')
    prepopulated_fields = {'slug': ('title', 'brand', 'category')}
