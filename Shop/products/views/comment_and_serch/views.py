from common.views import TitleMixin
from django.shortcuts import HttpResponseRedirect
from django.views import View
from django.views.generic import ListView
from products.models.product.models import Product
from products.services.comment.create import CommentCreateService
from products.services.serch.contextdata import ProductSerchContextDataService
from products.services.serch.queryset import ProductSerchQuerysetService
from users.forms import CommentForm


# Create your views here.


class ProductCommentView(View):

	def post(self, request, pk):
		form = CommentForm(request.POST)
		produc = Product.objects.get(id=pk)
		if form.is_valid():
			CommentCreateService.execute(
				{'product_id':produc.id,
				'user':request.user,
				'text':form.save(commit=False)})
		return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ProductSerchView(TitleMixin, ListView):
	template_name = 'products/products.html'

	def get_queryset(self):
		outcome = ProductSerchQuerysetService.execute({'find':self.request.GET.get("q")})
		return outcome

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		outcome = ProductSerchContextDataService.execute({'find':f'q={self.request.GET.get("q")}&'})
		context["q"] = outcome['find_name']
		return context

	title = 'ПродуктМаркет'


