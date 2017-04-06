from django import template
import json
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter
def to_char(value):
    return chr(96 + value)


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
