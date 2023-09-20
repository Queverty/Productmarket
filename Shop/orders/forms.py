from django import forms
from orders.models import Order


class OrederForm(forms.ModelForm):
	fio = forms.CharField(widget=forms.TextInput(attrs={
		'name': 'firstname', 'placeholder': 'Имя Фамилия Отчество'}))
	email = forms.CharField(widget=forms.TextInput(attrs={
		'name':'email','placeholder':'example@email.ru'}))
	addres = forms.CharField(widget=forms.TextInput(attrs={
		'name':'address','placeholder':'Томская 44-39'}))
	city = forms.CharField(widget=forms.TextInput(attrs={
		'name':'city','placeholder':'Москва'}))
	country = forms.CharField(widget=forms.TextInput(attrs={
		'name':'state','placeholder':'Россия'}))
	zip_code = forms.CharField(widget=forms.TextInput(attrs={
		'name':'zip','placeholder':'10001'}))
	class Meta:
		model = Order
		fields = ('fio', 'email', 'addres', 'city', 'country', 'zip_code')
