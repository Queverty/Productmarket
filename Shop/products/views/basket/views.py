from django.shortcuts import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView

from common.views import TitleMixin
from products.models.basket.models import Basket
from products.services.basket.add import BasketAddService
from products.services.basket.list import BasketListService
from products.services.basket.reduce import BasketReduceService
from products.services.basket.remove import BasketRemoveService


# Create your views here.
class BasketView(TitleMixin, ListView):
	template_name = 'products/basket.html'
	model = Basket
	title = "Корзина"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		outcome = BasketListService.execute({'user': self.request.user})
		context['total_sum'] = outcome['total_sum']
		context['basket'] = outcome['basket']
		return context


class BasketAddView(View):
	def get(self, request, product_id, *args, **kwargs):
		outcome = BasketAddService.execute({'user': request.user, 'product': product_id})
		return HttpResponseRedirect(request.META['HTTP_REFERER'], content=outcome)


class BasketReduceView(View):
	def get(self, request, product_id, *args, **kwargs):
		outcome = BasketReduceService.execute({'user': request.user, 'product': product_id})
		return HttpResponseRedirect(request.META['HTTP_REFERER'], content=outcome)


class BasketRemoveView(View):

	def get(self, request, basket_id, *args, **kwargs):
		outcome = BasketRemoveService.execute({'basket_id': basket_id})
		return HttpResponseRedirect(request.META['HTTP_REFERER'], content=outcome)
