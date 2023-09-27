from service_objects.services import Service
from django import forms
from products.models.basket.models import Basket


class BasketRemoveService(Service):
	basket_id = forms.IntegerField()

	def process(self, *args, **kwargs):
		basket = self.get_baskets.get(id=self.cleaned_data['basket_id'])
		basket.delete()
		return basket

	@property
	def get_baskets(self):
		return Basket.objects.all()
