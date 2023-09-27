from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

app_name = 'users'
urlpatterns = [
	path('login/', UserLoginView.as_view(), name='login'),
	path('register/', UserRegistrationView.as_view(), name='register'),
	path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('truereg/', SuccessfulRegistrationView.as_view(), name='truereg'),
	path('verify/<str:email>/<uuid:code>/', EmailVerifactionView.as_view(), name='verification'),
]
