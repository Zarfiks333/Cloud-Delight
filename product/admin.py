from django.contrib import admin
from .models import *

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'start_date', 'end_date', 'is_active', 'usage_limit', 'times_used')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('code',)

admin.site.register(PromoCode, PromoCodeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount', 'category', 'slug', 'is_best_seller')
    list_filter = ('category',) 
    search_fields = ('name', 'category__name', 'slug')
    prepopulated_fields = {"slug": ("name",)}  

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_disabled', 'description')
    list_filter = ('is_disabled',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}  

admin.site.register(Category, CategoryAdmin)


