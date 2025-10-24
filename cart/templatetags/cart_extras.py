# cart/templatetags/cart_extras.py
from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def delivery_remaining(total):
    threshold = 3000
    try:
        remaining = threshold - float(total)
        if remaining < 0:
            remaining = 0
        return int(remaining)
    except:
        return ''