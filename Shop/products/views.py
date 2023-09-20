from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect, render
from django.views import View
from django.views.generic import DetailView, ListView

from common.views import TitleMixin
from products.models.product.models import Product
from products.models.category.models import ProductCategory
from products.models.subcategory.models import ProductSubCategory
from products.models.basket.models import Basket
from users.models.comments.models import Comment
from users.forms import CommentForm


# Create your views here.

class ProductsListView(TitleMixin, ListView):
	model = Product
	template_name = 'products/products.html'
	title = 'ПродуктМакрет'

	def get_queryset(self):
		queryset = super(ProductsListView, self).get_queryset()
		subcategory_id = self.kwargs.get('subcategory_id')
		return queryset.filter(subcategory_id=subcategory_id) if subcategory_id else queryset

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProductsListView, self).get_context_data()
		context['categories'] = ProductCategory.objects.all()
		context['subcategories'] = ProductSubCategory.objects.all()
		return context


class ShowProdView(TitleMixin, DetailView):
	model = Product
	template_name = 'products/product_info.html'


class ProductCommentView(View):

	def post(self, request, pk):
		form = CommentForm(request.POST)
		produc = Product.objects.get(id=pk)
		if form.is_valid():
			form = form.save(commit=False)
			form.product_id = produc.id
			form.user_id = request.user.id
			form.save()
		return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ProductSerchView(TitleMixin,ListView):
	template_name = 'products/products.html'

	def get_queryset(self):
		return Product.objects.filter(name__icontains=self.request.GET.get("q"))

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context["q"] = f'q={self.request.GET.get("q")}&'
		return context

	title = 'ПродуктМаркет'

def basket(request):
	basket = Basket.objects.filter(user=request.user)
	total_sum = sum(bask.sum() for bask in basket)
	context = {'title': 'Корзина',
			   'baskets': basket,
			   'total_sum': total_sum,
			   }
	return render(request, 'products/basket.html', context)


@login_required
def basket_add(request, product_id):
	product = Product.objects.get(id=product_id)
	baskets = Basket.objects.filter(user=request.user, product=product)

	if not baskets:
		Basket.objects.create(user=request.user, product=product, quantity=1)
	else:
		basket = baskets.first()
		basket.quantity += 1
		basket.save()

	return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
	basket = Basket.objects.get(id=basket_id)
	basket.delete()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
