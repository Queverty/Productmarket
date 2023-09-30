from django import forms
from service_objects.fields import ModelField
from service_objects.services import Service

from products.models.basket.models import Basket
from products.models.product.models import Product
from users.models import User


class BasketReduceService(Service):
	user = ModelField(User)
	product = forms.IntegerField()

	def process(self, *args, **kwargs):
		produc = self.get_products.get(id=self.cleaned_data['product'])
		basket = self.get_baskets.filter(user=self.cleaned_data['user'], product=produc)
		bask = basket.first()
		if bask.quantity <= 1:
			bask.delete()
		else:
			bask.quantity -= 1
			bask.save()
		return bask

	@property
	def get_baskets(self):
		return Basket.objects.all()

	@property
	def get_products(self):
		return Product.objects.all()