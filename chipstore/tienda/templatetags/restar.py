from django import template

register = template.Library()

@register.filter
def restar(num, val):
    return num - val
