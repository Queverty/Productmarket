from common.views import TitleMixin
from django.views.generic import DetailView, ListView
from products.models.product.models import Product
from products.services.product.queryset import ProductQuerysetService
from products.services.product.contextdata import ProductContextDataService

# Create your views here.

class ProductsListView(TitleMixin, ListView):
	model = Product
	template_name = 'products/products.html'
	title = 'ПродуктМакрет'

	def get_queryset(self):
		outcome = ProductQuerysetService.execute({
			'subcategory_id': self.kwargs.get('subcategory_id', 0),
		})
		return outcome

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProductsListView, self).get_context_data()
		outcome = ProductContextDataService.execute({})
		context['categories'] = outcome['category']
		context['subcategories'] = outcome['subcategory']
		return context


class ShowProdView(TitleMixin, DetailView):
	model = Product
	template_name = 'products/product_info.html'







