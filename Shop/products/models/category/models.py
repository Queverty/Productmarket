from django.db import models

from products.models.basemodel.models import BaseModel


class ProductCategory(BaseModel):
	"""Category model"""
	name = models.CharField(max_length=128, unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"
