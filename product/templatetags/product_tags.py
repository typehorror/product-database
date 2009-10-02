from django import template
register = template.Library()

@register.filter
def gt(a, b):
    return a > b

@register.filter
def lt(a, b):
    return a < b
