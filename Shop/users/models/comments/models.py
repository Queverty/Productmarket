from django.db import models
from users.models.users.models import User
from products.models.product.models import Product
from products.models.basemodel.models import BaseModel

class Comment(BaseModel,models.Model):
	text = models.TextField()
	product = models.ForeignKey(to=Product,on_delete=models.CASCADE)
	user = models.ForeignKey(to=User,on_delete=models.CASCADE)

	def __str__(self):
		return self.text

	class Meta:
		app_label = 'users'