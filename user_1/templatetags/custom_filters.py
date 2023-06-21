from django import template

register = template.Library()

@register.filter()
def low(value):
	return value.lower()

@register.filter
def split(value, delimiter):
    return value.split(delimiter)