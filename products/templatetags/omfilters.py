'''Custom template filters.'''
from django.template import Library
from utils import utils

register = Library()

@register.filter
def format_price_usa(value):
    '''Format a number as an US currency.'''
    return utils.format_price_usa(value)

@register.filter
def cart_total_qty(cart):
    '''Returns the total quantity of each item's variation in the cart'''
    return utils.cart_total_qty(cart)