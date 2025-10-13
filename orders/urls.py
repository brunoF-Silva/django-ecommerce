from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.PayView.as_view(), name="pay"),
    path('placeorder/', views.PlaceOrderView.as_view(), name="placeorder"),
    path('detail/', views.OrderDetailView.as_view(), name="detail"),
]
