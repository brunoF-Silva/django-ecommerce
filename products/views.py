from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse

class ProductListView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("ProductList")

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
