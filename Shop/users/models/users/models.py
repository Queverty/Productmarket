from django.db import models
from products.models.basemodel.models import BaseModel
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser,BaseModel):
	phone = PhoneNumberField(null=True, blank=True)
	img = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)
	is_verified_email = models.BooleanField(default=False)
	email = models.EmailField(unique=True, null=True, blank=True)