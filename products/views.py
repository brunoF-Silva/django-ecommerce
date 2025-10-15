
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from .import models

class ProductListView(ListView):
    model = models.Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    paginate_by = 10

class ProductDetailView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("ProductDetail")

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
