from django import template

register = template.Library()


@register.filter
def split(value, separator):
    return value.split(separator)


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
