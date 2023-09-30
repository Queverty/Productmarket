import stripe
from django import forms
from django.http import HttpResponse
from service_objects.services import Service

from orders.models import Order
from Shop import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
class WebHookServices(Service):
	payload = forms.CharField()
	sig_header = forms.CharField()

	def process(self):
		payload = self.cleaned_data['payload']
		sig_header = self.cleaned_data['sig_header']
		event = None
		try:
			event = stripe.Webhook.construct_event(
				payload, sig_header, settings.STRIPE_WEBHOOK
			)
		except ValueError:
			return HttpResponse(status=400)
		except stripe.error.SignatureVerificationError:
			return HttpResponse(status=400)
		if event['type'] == 'checkout.session.completed':
			session = event['data']['object']

			self.fulfill_order(session)

		return HttpResponse(status=200)

	def fulfill_order(self, session):
		order_id = int(session.metadata.order_id)
		order = self.get_basket.get(id=order_id)
		order.update_after_payment()

	@property
	def get_basket(self):
		return Order.objects.all()
