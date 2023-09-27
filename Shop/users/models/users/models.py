from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from products.models.basemodel.models import BaseModel


class User(AbstractUser,BaseModel):
	phone = PhoneNumberField(null=True, blank=True)
	img = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)
	is_verified_email = models.BooleanField(default=False)
	email = models.EmailField(unique=True, null=True, blank=True)