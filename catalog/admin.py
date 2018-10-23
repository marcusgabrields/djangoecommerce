from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'created_at', 'updated_at']
    search_fields = ['name', 'slug']
    list_filter = ['created_at', 'updated_at']


class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'category', 'created_at', 'updated_at']
    search_fields = ['name', 'slug', 'category__name']
    list_filter = ['created_at', 'updated_at']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
