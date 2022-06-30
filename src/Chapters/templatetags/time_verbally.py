from django import template
from Chapters.service import get_time_verbally

register = template.Library()

@register.filter
def time_verbally(value):
    return get_time_verbally(value)
