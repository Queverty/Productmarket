from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from products.models import Product
from products.models.basket.models import Basket
from products.serializers import BasketSerializer, ProductSerializer
from products.services.basket.add import BasketAddService


# Create your views here.

class ProductModelViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


def get_permissions(self):
	if self.action in ('create', 'update', 'destroy'):
		self.permission_classes = (IsAdminUser,)
	return super(ProductModelViewSet, self).get_permissions()


class BasketModelViewSet(ModelViewSet):
	queryset = Basket.objects.all()
	serializer_class = BasketSerializer

	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		queryset = super(BasketModelViewSet, self).get_queryset()
		return queryset.filter(user=self.request.user)

	def create(self, request, *args, **kwargs):
		try:
			product_id = request.data['product_id']
			products = Product.objects.filter(id=product_id)
			if not products.exists():
				from rest_framework import status
				return Response({'product_id': 'Товара с таким ID не существует'}, status=status.HTTP_400_BAD_REQUEST)
			obj, is_created = BasketAddService(products.first().id, self.request.user)
			serializer = self.get_serializer(obj)
			return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
		except KeyError:
			return Response({'product_id': 'The field is required.'}, status=status.HTTP_400_BAD_REQUEST)
