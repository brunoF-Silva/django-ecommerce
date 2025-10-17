'''Utility functions.'''

def format_price_usa(value):
    '''Format a number as US currency.'''
    return f'${value:.2f}'

def format_price_br(value):
    '''Format a number as Brazilian currency.'''
    return f'R${value:.2f}'.replace('.', ',')

def cart_total_qty(cart):
    '''Return the total quantity of each item's variation in the cart'''
    return sum([item['quantity'] for item in cart.values()])

def cart_totals(cart):
    '''Return the total amount to be paid in the cart.
    
    Return the total amount to be paid considering each  
    item in the cart and whether they are on sale or not.
    '''
    return sum(
        [
            item.get('promotional_quantitative_pricing')
            if item.get('promotional_quantitative_pricing')
            else item.get('quantitative_pricing')
            for item
            in cart.values()
        ]
    )