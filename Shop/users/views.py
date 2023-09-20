from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegisterForm
from users.models.users.models import User
from users.models.usersemailverifications.models import EmailVerification

# Create your views here.

class UserLoginView(TitleMixin, LoginView):
	form_class = UserLoginForm
	template_name = 'users/login.html'
	title = "Авторизация"


class UserRegistrationView(TitleMixin, CreateView):
	model = User
	form_class = UserRegisterForm
	template_name = 'users/register.html'
	success_url = reverse_lazy('users:truereg')
	title = "Регистрация"


class UserProfileView(TitleMixin, UpdateView):
	model = User
	form_class = UserProfileForm
	template_name = 'users/profile.html'
	title = "Личный кабинет"

	def get_success_url(self):
		return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerifactionView(TitleMixin, TemplateView):
	title = "Подтверждение электронной почты"
	template_name = "users/user_verification.html"

	def get(self, request, *args, **kwargs):
		code = kwargs['code']
		user = User.objects.get(email=kwargs['email'])
		email_verifications = EmailVerification.objects.filter(user=user, code=code)
		if email_verifications.exists() and not email_verifications.first().is_expired():
			user.is_verified_email = True
			user.save()
			return super(EmailVerifactionView, self).get(request, *args, **kwargs)
		else:
			return HttpResponseRedirect(reverse('index'))


def trueregister(request):
	context = {"title": "Регистрация"}
	return render(request, "users/trueregister.html", context)
