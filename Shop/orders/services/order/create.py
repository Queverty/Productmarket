import stripe
from django import forms
from django.urls import reverse
from service_objects.fields import ModelField
from service_objects.services import Service

from products.models.basket.models import Basket
from Shop import settings
from users.models import User


class OrderCreateServices(Service):
	# basket = ModelField(Basket)
	user = ModelField(User)
	order = forms.IntegerField()

	def process(self):
		basket = self.get_basket.filter(user=self.cleaned_data['user'])
		checkout_session = stripe.checkout.Session.create(
			line_items=basket.stripe_products(),
			metadata={'order_id': self.cleaned_data['order']},
			mode='payment',
			success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:success')),
			cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:cancel')),
		)
		return checkout_session

	@property
	def get_user(self):
		return (User.objects.all())

	@property
	def get_basket(self):
		return Basket.objects.all()
