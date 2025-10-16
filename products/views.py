
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from .import models
from django.contrib import messages

class ProductListView(ListView):
    model = models.Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    paginate_by = 10

class ProductDetailView(DetailView):
    model = models.Product
    template_name = "product/product_detail.html"
    context_object_name = "product"
    slug_rul_kwarg = 'slug'


class AddToCartView(View):
    
    def get(self, *arg, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
            )
        variation_id = self.request.GET.get('vid')
        
        if not variation_id:
            messages.error(
                self.request,
                'Non-existent product'
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)

        return HttpResponse(f'{variation.product} {variation.name}')

class RemoveFromCartView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("RemoveFromCart")
class CartView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("CartView")
class CheckOutView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("CheckOut")
