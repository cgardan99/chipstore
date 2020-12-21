from django import template

register = template.Library()


@register.filter
def commapunto(val):
    val = str(val)
    return val.replace(',', '.')
