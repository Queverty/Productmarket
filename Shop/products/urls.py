from django.urls import path

from products.views.basket.views import BasketView, BasketRemoveView, BasketAddView, BasketReduceView
from products.views.comment_and_serch.views import ProductCommentView, ProductSerchView
from products.views.products.views import ProductsListView, ShowProdView

urlpatterns = [
	path('', ProductsListView.as_view(), name='index'),
	path('subcategory/<int:subcategory_id>/', ProductsListView.as_view(), name='categ'),
	path('products/<int:pk>/', ShowProdView.as_view(), name='products'),
	path('basket/', BasketView.as_view(), name='basket'),
	path('basket/add/<int:product_id>', BasketAddView.as_view(), name='basket_add'),
	path('basket/reduce/<int:product_id>', BasketReduceView.as_view(), name='basket_reduce'),
	path('basket/remove/<int:basket_id>', BasketRemoveView.as_view(), name='basket_remove'),
	path('comment/<int:pk>/', ProductCommentView.as_view(), name='comment'),
	path("search/", ProductSerchView.as_view(), name='search'),
]
