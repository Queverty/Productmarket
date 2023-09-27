from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField
from users.models.users.models import User


class EmailVerification(models.Model):
	code = models.UUIDField(unique=True)
	user = models.ForeignKey(to=User, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	expiration = models.DateTimeField()

	def __str__(self):
		return f'EmailVerification object {self.user.email}'

	def send_verifaction_email(self):
		link = reverse('users:verification', kwargs={'email': self.user.email, 'code': self.code})
		verification_link = f'{settings.DOMAIN_NAME}{link}'
		subject = f'Подтверждение учетной записи для {self.user.username}'
		message = 'Для подтверждение учетной записи для {} перейдите по ссылке: {}'.format(self.user.email,
																						   verification_link)
		send_mail(
			subject=subject,
			message=message,
			from_email=settings.EMAIL_HOST_USER,
			recipient_list=[self.user.email],
			fail_silently=False,
		)

	def is_expired(self):
		return True if now() >= self.expiration else False
