from django import template

register = template.Library()


@register.filter
def remove_trailing_zeros(number):
    return ('%.15f' % number).rstrip('0').rstrip('.')


@register.filter
def iso_format(value):
    return value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
