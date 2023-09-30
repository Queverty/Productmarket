from django.db import models

from products.models.basemodel.models import BaseModel
from products.models.category.models import ProductCategory


class ProductSubCategory(BaseModel):
	name = models.CharField(max_length=128, unique=True)
	category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Подкатегория"
		verbose_name_plural = "Подкатегории"
