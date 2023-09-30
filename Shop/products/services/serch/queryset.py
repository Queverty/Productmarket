from django import forms
from service_objects.services import Service

from products.models.product.models import Product


class ProductSerchQuerysetService(Service):
	find = forms.CharField()
	def process(self):
		products = self.get_products
		if self.cleaned_data['find']:
			products = products.filter(name__icontains=self.cleaned_data['find'])
		return products

	@property
	def get_products(self):
		return Product.objects.all()