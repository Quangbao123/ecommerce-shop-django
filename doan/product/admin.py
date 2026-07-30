from django.contrib import admin
from .models import Brand, Category, Product
# Register your models here.
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'name', 'price', 'id_category', 'id_brand', 'status', 'sale', 'company', 'image', 'detail')
