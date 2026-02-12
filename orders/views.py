from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from django.contrib import messages

from products.models import Variation
from .models import Order, OrderItem

from utils import utils

class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:create')
        
        return super().dispatch(*args, **kwargs)
    
class PaymentDetailView(DispatchLoginRequired, DetailView):
    template_name = 'order/payment.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs

class PlaceOrderView(View):
    template_name = 'order/payment.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'You need to log in.'
            )
            return redirect('profile:create')
        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Empty cart.'
            )
            return redirect('product:list')

        cart = self.request.session.get('cart')
        cart_variation_ids = [v for v in cart]
        bd_variations = list(
            Variation.objects.select_related('product')
            .filter(id__in=cart_variation_ids)
        )
        for variation in bd_variations:
            vid = str(variation.id)

            stock = variation.stock
            qtd_cart = cart[vid]['quantity']
            unit_price = cart[vid]['unit_price']
            promo_unit_price = cart[vid]['promotional_unit_price']

            error_msg_stock = ''

            if stock < qtd_cart:
                cart[vid]['quantity'] = stock
                cart[vid]['quantitative_pricing'] = stock * unit_price
                cart[vid]['promotional_quantitative_pricing'] = stock * \
                    promo_unit_price

                error_msg_stock = 'Insufficient stock for some products in your cart. '\
                    'We have reduced the quantity of these products. Please '\
                    'check which products were affected below.'

                if error_msg_stock:
                    messages.error(
                        self.request,
                        error_msg_stock
                    )

                    self.request.session.save()
                    return redirect('product:cart')

        cart_total_qty = utils.cart_total_qty(cart)
        cart_total_amount = utils.cart_totals(cart)

        order = Order(
            user=self.request.user,
            total=cart_total_amount,
            total_qty=cart_total_qty,
            status='C',
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_pricing'],
                    price_promo=v['promotional_quantitative_pricing'],
                    quantity=v['quantity'],
                    image=v['image'],
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']

        return redirect(
            reverse(
                'order:payment',
                kwargs={
                    'pk': order.pk,
                }
            )
        )

class OrderDetailView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("OrderDetail")


class ListOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("List")


