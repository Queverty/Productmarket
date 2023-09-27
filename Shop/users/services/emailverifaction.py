from service_objects.fields import ModelField
from service_objects.services import Service
from django import forms
from users.models import User
from users.models.usersemailverifications.models import EmailVerification


class EmailVerifactionServices(Service):
	code = forms.CharField()
	def process(self):
		email_verifications = self.get_emailv.filter(code=self.cleaned_data['code'])
		user_id=email_verifications.values_list()[0][2]
		user = self.get_user.get(id=user_id)
		if email_verifications.exists() and not email_verifications.first().is_expired():
			user.is_verified_email = True
			user.save()
		return {'user':user}

	@property
	def get_user(self):
		return User.objects.all()

	@property
	def get_emailv(self):
		return EmailVerification.objects.all()
