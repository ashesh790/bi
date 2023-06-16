from django import template

register = template.Library()


@register.filter
def split_string(value, delimiter, index):
    split_list = value.split(delimiter)
    return split_list[index]
