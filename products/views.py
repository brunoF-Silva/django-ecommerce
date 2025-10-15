
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from .import models

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
    def get(self, *args, **kwargs):
        return HttpResponse("AddToCart")

class RemoveFromCartView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("RemoveFromCart")
class CartView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("CartView")
class CheckOutView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("CheckOut")
