from django import forms
from service_objects.services import Service


class ProductSerchContextDataService(Service):
	find = forms.CharField()
	def process(self,*args, **kwargs):
		return {'find_name':self.cleaned_data['find']}