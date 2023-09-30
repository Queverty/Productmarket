from django.db import models

from products.models.basemodel.models import BaseModel
from products.models.product.models import Product
from users.models.users.models import User


class BasketQuerySet(models.QuerySet):
	def total_sum(self):
		return sum(basket.sum() for basket in self)

	def total_quantity(self):
		return sum(basket.quantity for basket in self)

	def stripe_products(self):
		line_items = []
		for basket in self:
			item = {
				'price': basket.product.stripe_product_price_id,
				'quantity': basket.quantity,
			}
			line_items.append(item)
		return line_items


class Basket(models.Model):
	user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)

	objects = BasketQuerySet.as_manager()

	def __str__(self):
		return f'Корзина'

	def sum(self):
		return self.product.price * self.quantity

	def de_json(self):
		basket_item = {
			'product_name':self.product.name,
			'quantity':self.quantity,
			'price': float(self.product.price),
			'sum': float(self.sum()),
		}
		return basket_item