'''Custom template filters.'''
from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_price_usa(value):
    '''Format a number as an US currency.'''
    return utils.format_price_usa(value)