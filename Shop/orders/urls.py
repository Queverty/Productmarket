from django.urls import path
from .views import *

app_name = 'orders'
urlpatterns = [path('create/', OrderCreateView.as_view(), name='create'),
			   path('success/', SuccessTemplateView.as_view(), name='success'),
			   path('', OrderListView.as_view(), name='order_list'),
			   path('order/<int:pk>', OrderDetailView.as_view(), name='order_info'),
			   ]
