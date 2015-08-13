from django import template
from math import log10, floor


register = template.Library()


@register.filter
def sigfigs(value, count):
    '''
    Returns the passed value as a float with <count> sigfigs.
    '''
    # round_to_n = lambda x, n:
    #     round(x, -int(floor(log10(x))) + (n - 1))
    if value == 0:
        return 0
    return round(value, -int(floor(log10(abs(value)))) + (count - 1))
