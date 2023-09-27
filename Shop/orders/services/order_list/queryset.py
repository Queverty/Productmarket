from service_objects.fields import ModelField
from service_objects.services import Service
from orders.models import Order
from users.models import User


class OrderQuerysetService(Service):
	user = ModelField(User)

	def process(self):
		order = self.get_order
		order = order.filter(initiator=self.cleaned_data['user'])
		return order

	@property
	def get_order(self):
		return Order.objects.all()
