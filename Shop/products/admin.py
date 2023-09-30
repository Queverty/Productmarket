from django.contrib import admin

from products.models.category.models import ProductCategory
from products.models.product.models import Product
from products.models.subcategory.models import ProductSubCategory

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(ProductSubCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name','price','quantity','subcategory')
	search_fields = ('name',)
	ordering = ('name',)