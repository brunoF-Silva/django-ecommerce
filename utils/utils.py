'''Utility functions.'''

def format_price_usa(value):
    '''Format a number as US currency.'''
    return f'${value:.2f}'

def format_price_br(value):
    '''Format a number as Brazilian currency.'''
    return f'R${value:.2f}'.replace('.', ',')
