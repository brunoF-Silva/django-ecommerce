from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.http import HttpResponse

class PayView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("Pay")

class PlaceOrderView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("PlaceOrder")
class OrderDetailView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("OrderDetail")


