from django import template

register = template.Library()


@register.filter
def remove_trailing_zeros(number):
    return ('%.15f' % number).rstrip('0').rstrip('.')
