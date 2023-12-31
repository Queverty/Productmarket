from django import forms
from service_objects.fields import ModelField
from service_objects.services import Service

from products.models.basket.models import Basket
from products.models.product.models import Product
from users.models import User


class BasketAddService(Service):
	user = ModelField(User)
	product = forms.IntegerField()

	def process(self, *args, **kwargs):
		produc = self.get_products.get(id=self.cleaned_data['product'])
		basket = self.get_baskets.filter(user=self.cleaned_data['user'], product=produc)
		if not basket:
			bask = basket.create(user=self.cleaned_data['user'], product=produc, quantity=1)
			is_created = True
			return bask,is_created
		else:
			bask = basket.first()
			bask.quantity += 1
			bask.save()
			is_created = False
			return bask,is_created


	@property
	def get_baskets(self):
		return Basket.objects.all()

	@property
	def get_products(self):
		return Product.objects.all()
