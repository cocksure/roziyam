from django.contrib import admin

from shop.models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name']
	search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'category', 'price', 'stock', 'available']
	list_filter = ['available', 'created', 'updated', 'category']
	list_editable = ['price', 'stock', 'available']
	search_fields = ['name', 'code']

	inlines = [ProductImageInline]
