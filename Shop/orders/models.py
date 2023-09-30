from django.db import models

from products.models.basket.models import Basket
from users.models.users.models import User

# Create your models here.

class Order(models.Model):
	CREATED = 0
	PAID = 1
	ON_WAY = 2
	DELIVERED = 3
	STATUSES = (
		(CREATED,"Создан"),
		(PAID,"Оплачен"),
		(ON_WAY,"В пути"),
		(DELIVERED,"Доставлен"),
	)

	fio = models.CharField(max_length=128)
	email = models.EmailField(max_length=128)
	addres = models.CharField(max_length=128)
	city = models.CharField(max_length=128)
	country = models.CharField(max_length=128)
	zip_code = models.CharField(max_length=128)
	basket_hitstory = models.JSONField(default=dict)
	created = models.DateTimeField(auto_now_add=True)
	status = models.PositiveSmallIntegerField(default=CREATED,choices=STATUSES)
	initiator = models.ForeignKey(to=User,on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.id}'

	def update_after_payment(self):
		baskets = Basket.objects.filter(user=self.initiator)
		self.status = self.PAID
		self.basket_hitstory = {
			'purchased_items': [basket.de_json() for basket in baskets],
			'total_sum': float(baskets.total_sum()),
		}
		baskets.delete()
		self.save()