"""
Views for the products application.

This module contains all the views related to product display and shopping
cart functionality. It includes class-based views for the main product
catalog (list and detail pages) and views to handle user interactions with
the session-based shopping cart, such as adding or removing items.
"""
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from .import models
from profiles.models import UserProfile

class ProductListView(ListView):
    """Displays a paginated list of all products."""
    model = models.Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    paginate_by = 10
    ordering = ['-id']
    
class SearchListView(ProductListView):
    def get_queryset(self, *args, **kwargs):
        term = self.request.GET.get('term') or self.request.session['term']
        qs = super().get_queryset(*args, **kwargs)
        
        if not term:
            return qs
        
        self.request.session['term'] = term
        
        qs = qs.filter(
            Q(name__icontains=term) |
            Q(short_description__icontains=term) |
            Q(long_description__icontains=term)
        )
        
        self.request.session.save()
        return qs
class ProductDetailView(DetailView):
    """Displays the details for a single product."""
    model = models.Product
    template_name = "product/product_detail.html"
    context_object_name = "product"
    slug_rul_kwarg = 'slug'


class AddToCartView(View):
    """
    Adds a product variation to the shopping cart stored in the 
    user's session.
    
    This view is triggered by a GET request containing a 'vid' 
    (variation ID) query parameter. It handles adding new items, 
    incrementing the quantity of existing items, and validating 
    against available stock.
    """
    def get(self, *arg, **kwargs):
        """
        Handles the GET request to add an item to the cart. Redirects the
        user back to their previous page with a success or error message.
        """
        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()
            
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
            )
        variation_id = self.request.GET.get('vid')
        
        
        if not variation_id:
            messages.error(
                self.request,
                'Non-existent product.'
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)
        variation_stock = variation.stock
        product = variation.product
        
        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        unit_price = variation.price
        promotional_unit_price = variation.promotional_price
        quantity = 1
        slug = product.slug
        image = product.image
        
        if variation.stock < 1:
            messages.error(
                self.request,
                'Out of stock'
            )
            return redirect(http_referer)
        
        if image:
            image = image.name
        else:
            image = ''
        
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()
            
        cart = self.request.session['cart']
        
        if variation_id in cart:
            cart_quantity = cart[variation_id]['quantity']
            cart_quantity += 1
                        
            if variation_stock < cart_quantity:
                messages.warning(
                    self.request,
                    f'Insufficient quantity for {cart_quantity}x on the '
                    f'"{product_name}" product. We\'ve added {variation_stock} '
                    f'to your shopping cart.'
                )
                cart_quantity = variation_stock
                
            cart[variation_id]['quantity'] = cart_quantity
            cart[variation_id]['quantitative_pricing'] = unit_price * \
                cart_quantity
            cart[variation_id]['promotional_quantitative_pricing'] = (
                promotional_unit_price * cart_quantity
            )

        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'promotional_unit_price': promotional_unit_price,
                'quantitative_pricing': unit_price,
                'promotional_quantitative_pricing': promotional_unit_price,
                'quantity': 1,
                'slug': slug,
                'image': image,
            }
            
        self.request.session.save()
        
        messages.success(
            self.request,
            f'Product "{product_name} {variation_name}" added to your '
            f'shopping cart {cart[variation_id]["quantity"]}x.'
        )
        
        return redirect(http_referer)

class RemoveFromCartView(View):
    '''Remove from cart operation'''
    def get(self, *args, **kwargs):
        '''Method to handle the items in the user session'''
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')
        
        if not variation_id:
            return redirect(http_referer)
        
        if not self.request.session.get('cart'):
            return redirect(http_referer)
        
        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)
        
        cart = self.request.session['cart'][variation_id]
        
        messages.success(
            self.request,
            f'Product "{cart["product_name"]} - {cart["variation_name"]}" '
            f'removed from your cart.'
        )
        
        del self.request.session['cart'][variation_id]
        self.request.session.save()
        return redirect(http_referer)
        
class CartView(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {})
        }
        return render(self.request, 'product/cart.html', context)
class CheckoutView(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profile:create')
        
        profile = UserProfile.objects.filter(user=self.request.user).exists()
        
        if not profile:
            messages.error(
                self.request,
                'User without a profile.'
            )
            return redirect('profile:create')
        
        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Empty cart.'
            )
            return redirect('product:list')
        
        if not self.request.user.is_authenticated:
            return redirect('profile:create')
                
        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
        }

        return render(self.request, 'product/checkout.html', context)
