from django.core.cache import cache
from django.conf import settings
from .models import Category

def get_categories():
    if settings.CACHE_ENABLED:
        key = 'category_list'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list, 60 * 15)
    else:
        category_list = Category.objects.all()
    
    return category_list 