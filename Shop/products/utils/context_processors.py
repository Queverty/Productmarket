from products.models.basket.models import Basket
from products.models.category.models import ProductCategory
from products.models.subcategory.models import ProductSubCategory


def category_context(request):
    return {'categories': ProductCategory.objects.all(),
            'subcategories': ProductSubCategory.objects.all(),}

def baskets(request):
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}
