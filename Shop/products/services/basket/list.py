from service_objects.fields import ModelField
from service_objects.services import Service

from products.models.basket.models import Basket
from users.models import User


class BasketListService(Service):
	user = ModelField(User)

	def process(self, *args, **kwargs):
		basket = self.get_baskets
		basket = basket.filter(user=self.cleaned_data['user'])
		return {'basket': basket, 'total_sum': self.total_sum}

	@property
	def get_baskets(self):
		return Basket.objects.all()

	@property
	def total_sum(self):
		basket = self.get_baskets
		basket = basket.filter(user=self.cleaned_data['user'])
		return sum(bask.sum() for bask in basket)
