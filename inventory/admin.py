from django.contrib import admin
from .models import Category, Product, Store
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'is_low_stock')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'owner', 'created_at')
    search_fields = ('name', 'owner__username')  # You can search by store name or store owner's username



