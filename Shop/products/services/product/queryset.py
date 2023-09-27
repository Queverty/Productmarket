from service_objects.services import Service
from django import forms

from products.models.product.models import Product


class ProductQuerysetService(Service):
	subcategory_id = forms.IntegerField()

	def process(self):
		products = self.get_products
		if self.cleaned_data['subcategory_id']:
			products = products.filter(subcategory_id=self.cleaned_data['subcategory_id'])
		return products
	@property
	def get_products(self):
		return Product.objects.all()