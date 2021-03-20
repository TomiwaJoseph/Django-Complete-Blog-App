from django import template
from ..models import Blog

register = template.Library()

@register.filter
def lookup(d, key):
    return d[key]

