from rest_framework import serializers
from products.models import Product
from products.models.category.models import ProductCategory


class ProductSerializer(serializers.ModelSerializer):
	subcategory = serializers.SlugRelatedField(slug_field='name',queryset=ProductCategory.objects.all())
	class Meta:
		model = Product
		fields = ('id', 'name', 'decription', 'price', 'quantity', 'image', 'subcategory')
