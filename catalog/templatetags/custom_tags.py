from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def mediapath(value):
    """
    Преобразует путь к медиафайлу в полный путь
    """
    if value:
        return f"{settings.MEDIA_URL}{value}"
    return "" 