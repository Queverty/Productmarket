from django.urls import path

from .views import *

urlpatterns = [
	path('', ProductsListView.as_view(), name='index'),
	path('category/<int:subcategory_id>/', ProductsListView.as_view(), name='categ'),
	path('products/<int:pk>/', ShowProdView.as_view(), name='products'),
	path('basket/', basket, name='basket'),
	path('basket/add/<int:product_id>', basket_add, name='basket_add'),
	path('basket/remove/<int:basket_id>', basket_remove, name='basket_remove'),
	path('comment/<int:pk>/', ProductCommentView.as_view(), name='comment'),
	path("search/", ProductSerchView.as_view(), name='search'),
]
