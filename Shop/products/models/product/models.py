import stripe
from django.conf import settings
from django.db import models
from products.models.basemodel.models import BaseModel
from products.models.subcategory.models import ProductSubCategory

stripe.api_key = settings.STRIPE_SECRET_KEY


class Product(BaseModel):
	name = models.CharField(max_length=256, unique=True)
	decription = models.TextField()
	price = models.DecimalField(max_digits=6, decimal_places=2)
	quantity = models.PositiveIntegerField(default=0)
	image = models.ImageField(upload_to="photos/%Y/%m/%d/")
	stripe_product_price_id = models.CharField(max_length=256, null=True, blank=True)
	subcategory = models.ForeignKey(to=ProductSubCategory, on_delete=models.CASCADE)

	def __str__(self):
		return self.name



	class Meta:
		verbose_name = "Продукт"
		verbose_name_plural = "Продукты"

	def create_stripe_product_price(self):
		stripe_product = stripe.Product.create(name=self.name)
		stripe_product_price = stripe.Price.create(
			product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub')
		return stripe_product_price

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if not self.stripe_product_price_id:
			stripe_prod_price = self.create_stripe_product_price()
			self.stripe_product_price_id = stripe_prod_price['id']
		super(Product,self).save(force_insert=False, force_update=False, using=None, update_fields=None)

