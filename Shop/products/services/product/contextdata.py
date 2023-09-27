from service_objects.services import Service
from products.models.category.models import ProductCategory
from products.models.subcategory.models import ProductSubCategory


class ProductContextDataService(Service):

	def process(self):
		return {
			'category': self.get_category,
			'subcategory': self.get_subcategory,
		}

	@property
	def get_category(self):
		return ProductCategory.objects.all()

	@property
	def get_subcategory(self):
		return ProductSubCategory.objects.all()
