from django.contrib import admin
from orders.forms import Order

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'status')
	fields = (
		'id', 'created',
		'fio',
		'email', 'addres',
		'basket_hitstory', 'status', 'initiator',
	)
	readonly_fields = ('id', 'created')