from django import template
from chapters.service import get_time_verbally

register = template.Library()

@register.filter
def time_verbally(value):
    return get_time_verbally(value)
