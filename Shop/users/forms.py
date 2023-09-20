import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
									   UserCreationForm)
from django.utils.timezone import now

from users.models.users.models import User
from users.models.usersemailverifications.models import EmailVerification
from users.models.comments.models import Comment

class CommentForm(forms.ModelForm):
	text = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-box'}))

	class Meta:
		model = Comment
		fields = ['text']


class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={
		'type': "text",
		'placeholder': "Введите email"
	}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={
		'type': "password",
		'placeholder': "Введите пароль"
	}))

	class Meta:
		model = User
		fields = ("username", "password")


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={
		'type': "text",
		'placeholder': "Введите логин"
	}))
	phone = forms.CharField(widget=forms.TextInput(attrs={
		'type': "text",
		'placeholder': "Введите номер телефона"
	}))
	email = forms.CharField(widget=forms.TextInput(attrs={
		'type': "text",
		'placeholder': "Введите email"
	}))
	password2 = forms.CharField(widget=forms.TextInput(attrs={
		'type': "password",
		'placeholder': "Повторите пароль"
	}))
	password1 = forms.CharField(widget=forms.TextInput(attrs={
		'type': "password",
		'placeholder': "Введите пароль"
	}))

	class Meta:
		model = User
		fields = ('username', 'phone', 'password1', 'password2', 'email')

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=True)
		expiration = now() + timedelta(hours=24)
		record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
		record.send_verifaction_email()
		return user


class UserProfileForm(UserChangeForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-box'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-box'}))
	image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'input-box'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-box', 'readonly': True}))
	email = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-box', 'readonly': True}))
	phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-box'}))

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'image', 'username', 'email', 'phone', 'is_verified_email')
