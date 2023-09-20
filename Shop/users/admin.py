from django.contrib import admin
from products.models.basket.models import Basket
from users.models.users.models import User
from users.models.usersemailverifications.models import EmailVerification
from users.models.comments.models import Comment

# Register your models here.

admin.site.register(Comment)

class BasketAdmin(admin.TabularInline):
	model = Basket
	list_display = ('product', 'quantity')
	extra = 0


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'first_name', 'last_name')
	inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
	list_display = ('code', 'user', 'expiration')
	fields = ('code', 'user', 'expiration', 'created')
	readonly_fields = ('created',)
