from service_objects.services import Service
from django import forms
from products.models.product.models import Product
from users.models import User
from users.models import Comment
from service_objects.fields import ModelField


class CommentCreateService(Service):
	text = forms.CharField()
	product_id = forms.IntegerField()
	user = ModelField(User)

	def process(self):
		self.result = self._create_comment()
		return self

	def _create_comment(self):
		product = Product.objects.get(id=self.cleaned_data['product_id'])
		comment = Comment(
			product=product,
			text=self.cleaned_data['text'],
			user_id=self.cleaned_data['user'].id,
		)
		comment.save()
		return comment
