from django.contrib import admin

# Register your models here.
from .models import Product, Category
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_available', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('is_available', 'category')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)