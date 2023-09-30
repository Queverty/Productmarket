from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrederForm
from orders.models import Order
from orders.services.order.create import OrderCreateServices
from orders.services.order_list.queryset import OrderQuerysetService

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
	template_name = 'orders/order_success.html'
	title = "Спасибо за заказ"


class CancelTemplateView(TitleMixin, TemplateView):
	template_name = 'orders/order_cancel.html'
	title = "Заказ отменен"


class OrderDetailView(DetailView):
	template_name = 'orders/order_detail.html'
	model = Order


class OrderListView(TitleMixin, ListView):
	template_name = 'orders/orders.html'
	title = "История заказов"
	ordering = ('-id')

	def get_queryset(self):
		outcome = OrderQuerysetService.execute({'user': self.request.user})
		return outcome


class OrderCreateView(TitleMixin, CreateView):
	template_name = 'orders/order_create.html'
	form_class = OrederForm
	success_url = reverse_lazy('orders:create')
	title = 'Оформление заказа'

	def post(self, request, *args, **kwargs):
		super(OrderCreateView, self).post(request, *args, **kwargs)
		outcome = OrderCreateServices.execute({'user': self.request.user, 'order': self.object.id})
		return HttpResponseRedirect(outcome.url, status=HTTPStatus.SEE_OTHER)

	def form_valid(self, form):
		form.instance.initiator = self.request.user
		return super(OrderCreateView, self).form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
	payload = request.body
	sig_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None

	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, settings.STRIPE_WEBHOOK
		)
	except ValueError:
		# Invalid payload
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError:
		# Invalid signature
		return HttpResponse(status=400)

	# Handle the checkout.session.completed event
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']

		# Fulfill the purchase...
		fulfill_order(session)

	# Passed signature verification
	return HttpResponse(status=200)


def fulfill_order(session):
	order_id = int(session.metadata.order_id)
	order = Order.objects.get(id=order_id)
	order.update_after_payment()
